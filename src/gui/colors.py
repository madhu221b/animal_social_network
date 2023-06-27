import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def bandfilter_colormap(cmap, filter1=0.4, filter2=0.6, n=100):
    filter = np.linspace(0, filter1, n//2).tolist() + np.linspace(filter2, 1, n//2).tolist()
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'bandfilter({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=filter1, b=filter2),
        cmap(filter))
    return new_cmap

# cmap = plt.get_cmap("terrain")
# cmap1 = truncate_colormap(cmap, 0., 0.7)
# cmap1_str = "terrain"

cmap1 = bandfilter_colormap(plt.get_cmap("Spectral_r"))
cmap1_str = "Spectral_r"

