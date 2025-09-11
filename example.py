from imagetune import tune, tuneui
from skimage import data
from skimage.filters import gaussian, unsharp_mask

@tune(min=0, max=1.0)
def threshold(im, t1):
    return im > t1

@tune(argnums=(1, 2))
def adjust(im, alpha, gamma):
    return alpha * im**gamma


def preprocess(im):
    im = adjust(im, 1.0, 1.0)
    im = tune(gaussian)(im, 1.0)
    im = tune(unsharp_mask, argnames='amount')(im, radius=2.0, amount=1.0)
    im = threshold(im, 0.5)
    return im



if __name__ == '__main__':
    im = data.astronaut()[:, :, 0] / 255.
    tuneui(preprocess, im)
