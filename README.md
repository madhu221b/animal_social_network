## Installation Guide
```bash
conda create -n mma python=3.9
conda activate mma

pip install pyqt5
pip install netgraph
pip install mycolorpy

conda clean --all
```

## Launching Dashboard 
```bash
python src/dashboard/main.py
```

## Downloading the data
Download [this](https://drive.google.com/file/d/1HSvRDI7EV1w1UDJNo65v7-AYT9HLaOm9/view?usp=sharing) file and run the following commands to clone the ASNR repo and move the data into the `datasets/` folder. 

```bash
git clone https://github.com/bansallab/asnr.git
python scripts/move_asnr.py
```

## Training Graph-VAE Model 
```bash
python src/dashboard/models/train.py --animal <<animal_name>>
```

