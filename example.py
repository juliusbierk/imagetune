from imagetuner import tune, tuneui
from skimage import data
from skimage.filters import gaussian


@tune(min=0, max=1.0)
def threshold(im, t1):
    return im > t1


def preprocess(im):
    im = tune(gaussian, min=0.0, max=5.0)(im, 0.0)
    im = threshold(im, 0.5)
    return im


if __name__ == '__main__':
    im = data.astronaut()[:, :, 0] / 255.
    tuneui(preprocess, im)
