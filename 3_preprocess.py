import os
import argparse
import numpy as np
import nibabel as nib

from glob import glob
from tqdm import tqdm


def main(args):
    cadaver_list = glob(args.input + '/*')
    
    for cadaver in tqdm(cadaver_list):
        cadaver_id = os.path.basename(cadaver)
        path_ct = os.path.join(cadaver, f'{cadaver_id}.nii.gz')
        path_seg = glob(os.path.join(cadaver, f'{cadaver_id}_*bone_mask*.nii.gz'))[0]

        ct_img = nib.load(path_ct)
        seg_img = nib.load(path_seg)

        ct_data = ct_img.get_fdata()
        seg_data = seg_img.get_fdata()

        z_slices = seg_data.shape[2]
        ct_cropped = ct_data[:, :, :z_slices]

        os.makedirs(os.path.join(args.output, cadaver_id), exist_ok=True)
        cropped_ct_path = os.path.join(args.output, f'{cadaver_id}/{cadaver_id}.nii.gz')
        seg_path = os.path.join(args.output, f'{cadaver_id}/{cadaver_id}_seg.nii.gz')

        nib.save(nib.Nifti1Image(ct_cropped, ct_img.affine, ct_img.header), cropped_ct_path)
        nib.save(nib.Nifti1Image(seg_data, seg_img.affine, seg_img.header), seg_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess DICOM files')

    parser.add_argument('--input', type=str, help='Input directory', default='2_CTPEL_nii')
    parser.add_argument('--output', type=str, help='Output directory', default='3_CTPEL_preprocessed')

    args = parser.parse_args()

    main(args)