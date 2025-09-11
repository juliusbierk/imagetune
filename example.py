from imagetune import tune, tuneui
from skimage import data
from skimage.filters import gaussian

@tune(min=0, max=1.0)
def threshold(im, t1):
    return im > t1

@tune
def gamma(im, gamma):
    return im**gamma

# @tune(argnums=(1, 2))
def adjust(im, alpha, gamma):
    return alpha * im**gamma

@tune(argnames=('alpha', 'gamma'))
def adjust2(im, alpha, gamma):
    return alpha * im**gamma


def preprocess(im):
    im = tune(adjust, argnums=(1, 2))(im, alpha=0.5, gamma=1.0)
    im = tune(adjust, argnames='gamma')(im, 0.5, gamma=1.0)

    #
    # im = tune(gaussian, min=0.0, max=15.0)(im, 0.0)
    # im = gamma(im, 1.0)
    # im = tune(gaussian, min=0.0, max=5.0)(im, 0.0)
    # im = adjust2(im, 0.5, 1.0)
    # im = adjust2(im, alpha=0.5, gamma=1.0)
    # im = threshold(im, 0.5)
    return im


if __name__ == '__main__':
    im = data.astronaut()[:, :, 0] / 255.
    tuneui(preprocess, im)
