import os
import shutil
import argparse

from glob import glob
from tqdm import tqdm


def main(args):
    unzipped_file_list = glob(args.input + '/*')
    
    for unzipped_file in tqdm(unzipped_file_list):
        case_id = unzipped_file.split('/')[-1]

        dicom_dir = f'{unzipped_file}/im_1_decompressed'
        dicom_file = sorted(glob(f'{dicom_dir}/*'))[0]
        
        # Copy DICOM file to output directory
        output_dir = f'{args.output}/{case_id}'
        os.makedirs(output_dir, exist_ok=True)
        shutil.copy(dicom_file, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess DICOM files')

    parser.add_argument('--input', type=str, help='Input directory', default='1_CTPEL_unzipped')
    parser.add_argument('--output', type=str, help='Output directory', default='3_CTPEL_preprocessed')

    args = parser.parse_args()

    main(args)