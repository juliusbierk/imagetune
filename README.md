# IMAGETUNE

`imagetune` is a simple GUI to interactively tune image-processing parameters.
It utilizes the hardware accellerated speed of ![fastplotlib](https://github.com/fastplotlib/fastplotlib) to provide visual feedback that is not limited by plotting.

`imagetune` is simple to use requiring only minimal changes to your code. Simply wrap the functions you wish to tune the parameters of with `tune` and launch `tuneui`.

![ImageTune](https://github.com/juliusbierk/imagetune/blob/main/.github/imgs/code.png)

### How to use
Here is a simple script to make a binary version of an image:

```python
from skimage.filters import gaussian
from skimage import data


def threshold(im, thres_val):
    return im > thres_val


def preprocessing(im):
    bg = gaussian(im, 10)
    fg = im - bg
    segmented = threshold(fg, 0.1)
    return segmented


im = data.coins()
result = preprocessing(im)
```

The script depends on parameters, `sigma=10` for Gaussian filtering and `thres_val=0.1` for the thresholding.
In order to tune these live, simply wrap those functions in `tune`:

```diff
from skimage.filters import gaussian
from skimage import data
+from imagetune import tune, tuneui


def threshold(im, thres_val):
    return im > thres_val


def preprocessing(im):
-    bg = gaussian(im, 10)
+    bg = tune(gaussian)(im, 10)
     fg = im - bg
-    segmented = threshold(fg, 0.1)
+    segmented = tune(threshold)(fg, 0.1)
    return segmented


im = data.coins()
+tuneui(preprocessing, im)
```

This launches a small window in which the parameters are tunable live:

![ImageTune](https://github.com/juliusbierk/imagetune/blob/main/.github/imgs/example1.png)

You can also decorate your functions instead

```diff
+@tune
def threshold(im, thres_val):
    return im > thres_val
```

Note that the function still works as normal:

```python
output = preprocessing(im)
```

Only when you run `tuneui(preprocessing, im)` does it behave differently.


## Installation

Install directly with `pip`:

```bash
pip install imagetune
```

## Function requirements

All tunable functions are asssumed to take an image as its input and return an image as its output.

## Choosing parameters

Given a function:

```python
def adjust(im, alpha, gamma):
    return alpha * im**gamma
```

The decorator `tune` will per standard assume you wish to tune the first parameter (`alpha`).
You can change this by specifying `argnames`:

```python
tune(adjust, argnames='gamma')
```

or `argnums`:

```python
tune(adjust, argnums=2)
```

The behavior of the above is identical.
You can also tune both parameters, by either

```python
tune(adjust, argnames=('alpha', 'gamma'))
```

or

```python
tune(adjust, argnums=(1, 2))
```

## Misc

To overwrite function names in the UI, simply pass along a name:
```python
bg = tune(gaussian, name='blur')(im, 10)
```

You can also choose a `min`, `max` of the parameter bar:
```python
bg = tune(gaussian, min=0, max=300)(im, 10)
```
