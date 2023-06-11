
"""
Usage :  python train.py --animal bat

"""
import numpy as np
import torch
from argparse import ArgumentParser

import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)


from dashboard.canvas import an2tex

def train_model(animal):
    path = an2tex[animal]
    print(path)
if __name__ == '__main__':
    argp = ArgumentParser()

    argp.add_argument('--seed', default=0, type=int)
    argp.add_argument('--animal', default="bat")

    
    args = argp.parse_args()
    if args.seed:
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)

    train_model(args.animal)
    
    