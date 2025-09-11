from imagetune import tune, tuneui
from skimage import data
from skimage.filters import gaussian

# TODO:
#  update API to allow multiple parameters per function

@tune(min=0, max=1.0)
def threshold(im, t1):
    return im > t1

@tune
def gamma(im, gamma):
    return im**gamma


def preprocess(im):
    im = tune(gaussian, min=0.0, max=15.0)(im, 0.0)
    im = gamma(im, 1.0)
    im = tune(gaussian, min=0.0, max=5.0)(im, 0.0)
    im = threshold(im, 0.5)
    return im


if __name__ == '__main__':
    im = data.astronaut()[:, :, 0] / 255.
    tuneui(preprocess, im)
