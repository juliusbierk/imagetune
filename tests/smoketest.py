from PyQt6 import QtCore
import pytest
from skimage import data

from imagetune.imagetune import _tune_ui_widget
from imagetune import tune


def adjust(im, alpha, gamma):
    return alpha * im**gamma

@tune(argnums=(2, ))
def adjust2(im, alpha, gamma):
    return alpha * im**gamma

@tune
def adjust3(im, alpha, gamma):
    return alpha * im**gamma

@tune
def adjust4(im, alpha, gamma=2.0):
    return alpha * im**gamma


def preprocess(im):
    im = tune(adjust)(im, alpha=0.5, gamma=1.0)
    im = tune(adjust, argnames='gamma')(im, alpha=0.5, gamma=1.0)
    im = tune(adjust, argnums=(1, 2))(im, alpha=0.5, gamma=1.0)
    im = tune(adjust, argnames='gamma')(im, 0.5, 1.0)
    im = tune(adjust, argnums=(1, 2))(im, 0.5, gamma=1.0)
    im = adjust2(im, 0.5, gamma=1.0)
    im = adjust3(im, 0.5, 1.0)
    im = adjust4(im, 0.5)
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
