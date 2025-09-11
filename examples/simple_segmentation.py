from skimage.filters import gaussian
from skimage import data
from skimage.measure import label
from skimage.color import label2rgb
from skimage.morphology import binary_closing, disk
from skimage.segmentation import clear_border

from imagetune import tune, tuneui


def threshold(im, thres_val):
    return im > thres_val


def close(im, radius):
    return binary_closing(im, disk(radius))


def preprocessing(im):
    bg = tune(gaussian)(im, 10)
    fg = im - bg
    segmented = tune(threshold)(fg, 0.1)
    closed = tune(close)(segmented, 5)
    closed = clear_border(closed)
    return label2rgb(label(closed))


im = data.coins()
tuneui(preprocessing, im)

