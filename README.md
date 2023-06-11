## Installation Guide
```bash
conda create -n mma python=3.9
conda activate mma

pip install pyqt5
pip install netgraph

conda clean --all
```

## Launching Dashboard 
```bash
python src/dashboard/main.py
```

## Training Graph-VAE Model 
```bash
python src/dashboard/models/train.py --animal <<animal_name>>
```

