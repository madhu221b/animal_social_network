import random, os
import numpy as np
import torch


def swap_dict_keys(dict_sample):
    d = {}
    # for each key and sub-dict in the main dict
    for k1, s in dict_sample.items():
        # for each key and value in the sub-dict
        for k2, v in s.items():
            # this is equivalent to d[k2][k1] = int(v), except that when k2 is not yet in d,
            # setdefault will initialize d[k2] with {} (a new dict)
            d.setdefault(k2, {})[k1] = v
    return d


def seed_everything(seed: int):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True