from PyQt6 import QtCore
import pytest
from skimage import data
from skimage.filters import gaussian, unsharp_mask

from imagetune.imagetune import _tune_ui_widget
from imagetune import tune


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

@pytest.mark.parametrize("show_window", [True, False])
def test_main_widget_starts_and_closes(qtbot, show_window):
    im = data.astronaut()[:, :, 0] / 255.0
    w = _tune_ui_widget(preprocess, im)

    qtbot.addWidget(w)

    if show_window:
        w.show()
        try:
            qtbot.waitExposed(w, timeout=3000)
        except Exception:
            pass  # okay on offscreen

    qtbot.wait(100)

    w.close()
