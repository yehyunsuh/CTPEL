import os
import argparse

from glob import glob


def main(args):
    zip_file_list = glob(args.input + '/*.zip')

    for zip_file in zip_file_list:
        file_name = os.path.basename(zip_file).split('.zip')[0]

        # Unzip the zip file to the output directory
        os.system(f"unzip '{zip_file}' -d '{args.output}/{file_name}'")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unzip zip files')

    parser.add_argument('--input', type=str, help='Input zip directory', required=True, default=None)
    parser.add_argument('--output', type=str, help='Output unzipped directory', default='1_CTPEL_unzipped')

    args = parser.parse_args()

    os.makedirs(f'{args.output}', exist_ok=True)

    main(args)