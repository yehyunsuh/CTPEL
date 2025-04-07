"""
The dicom files were compressed using JPEG 2000 Lossless (transfer syntax UID 1.2.840.10008.1.2.4.90).
By default, dcm2niix does not support decompression of JPEG 2000-compressed DICOM images.
Therefore, we need to decompress the DICOM files before converting them to NIfTI format.
If we do not decompress them, you will see the same error as below
```
Warning: Unsupported transfer syntax '1.2.840.10008.1.2.4.90' (see www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage)
```
"""

import os
import json
import pydicom
import argparse
import subprocess
import numpy as np

from glob import glob
from tqdm import tqdm


def main(args):
    unzipped_file_list = glob(args.input + '/*')
    
    for unzipped_file in unzipped_file_list:
        print(f'Processing unzipped file: {unzipped_file}')
        case_id = unzipped_file.split('/')[-1]
        subdirectory_list = glob(f'{unzipped_file}/*')

        for subdirectory in subdirectory_list:
            if 'im_1' in subdirectory and 'decompressed' not in subdirectory:
                # Decompress DICOM files
                decompressed_dcm_dir = f'{args.input}/{case_id}/{subdirectory.split("/")[-1]}_decompressed'
                if not any('im_1_decompressed' in subdir for subdir in subdirectory_list):
                    os.makedirs(decompressed_dcm_dir, exist_ok=True)

                    dicom_files = glob(f'{subdirectory}/*.dcm')
                    for file in tqdm(dicom_files):
                        output_file = os.path.join(decompressed_dcm_dir, os.path.basename(file))
                        cmd = [
                            "gdcmconv", "--raw", "--force", "--verbose",
                            "-i", file, "-o", output_file
                        ]
                        subprocess.run(cmd, check=True)

                # Convert decompressed DICOM to NIfTI using dcm2niix
                nifti_output_dir = os.path.join(args.output, case_id)
                os.makedirs(nifti_output_dir, exist_ok=True)

                os.system(f'dcm2niix -o "{args.output}/{case_id}" -f "{case_id}" -z y -s y "{decompressed_dcm_dir}"')

            elif 'im_3' in subdirectory:
                # Bone Segmentation
                segmentation_dcm = f'{subdirectory}/x0000.dcm'
                os.system(f'segimage2itkimage -t nifti --mergeSegments --inputDICOM "{segmentation_dcm}" --outputDirectory "{args.output}/{case_id}" -p {case_id}_bone_mask')

            elif 'im_4' in subdirectory:
                # Anatomical Landmarks
                dcm_file = f'{subdirectory}/x0000.dcm'
                dicom_file = pydicom.dcmread(dcm_file)
                
                landmarks = []
                if hasattr(dicom_file, "GraphicAnnotationSequence"):
                    for annotation in dicom_file.GraphicAnnotationSequence:
                        if hasattr(annotation, "TextObjectSequence"):
                            for text_obj in annotation.TextObjectSequence:
                                name = text_obj.UnformattedTextValue if hasattr(text_obj, "UnformattedTextValue") else "Unknown"
                                coords = text_obj.AnchorPoint if hasattr(text_obj, "AnchorPoint") else None
                                
                                if coords:
                                    landmarks.append({"name": name, "coordinates": coords})
                                                    
                json_file_path = os.path.join(args.output, f'{case_id}/{case_id}_landmarks.json')
                with open(json_file_path, 'w') as json_file:
                    json.dump(landmarks, json_file, indent=4)
                
            else:
                pass
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert DICOM to NIfTI')

    # Argument for directory
    parser.add_argument('--input', type=str, help='Input unzipped directory', default='1_CTPEL_unzipped')
    parser.add_argument('--output', type=str, help='Output NIfTI directory', default='2_CTPEL_nii')

    args = parser.parse_args()

    main(args)