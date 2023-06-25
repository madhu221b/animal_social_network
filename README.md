## Installation Guide
```bash
conda create -n mma python=3.9
conda activate mma

pip install pyqt5
pip install netgraph
pip install mycolorpy
pip install holoviews

conda clean --all
```

## Launching Dashboard 
```bash
python src/dashboard/main.py
```

## Downloading the data
Download [this](https://drive.google.com/file/d/1HSvRDI7EV1w1UDJNo65v7-AYT9HLaOm9/view?usp=sharing) file, place it in the `./datasets` directory and clone the ASNR repo with the following command: 

```bash
git clone https://github.com/bansallab/asnr.git
```

## Training Graph-VAE Model 
```bash
python src/dashboard/models/train.py --animal <<animal_name>>
```

