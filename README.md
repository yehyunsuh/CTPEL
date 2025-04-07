# CTPEL

```
conda create -n CTPEL python=3.10 -y
conda activate CTPEL
pip3 install -r requirements.txt
```

## 0. Download CTPEL dataset

## 1. Unzip CTPEL dataset
```
python3 1_unzip.py
```

## 2. Convert dcm to nii.gz
```
pip3 install dcm2niix dcmqi
python3 2_dcm2nii.py
```