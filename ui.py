import numpy as np
from skimage import data, color, exposure, filters
import fastplotlib as fpl
from PySide6 import QtWidgets, QtCore
from functools import partial


def _from_slider(val, min, max):
    return min + val / 100.0 * (max - min)


def _to_slider(val, min, max):
    return int(100 * (val - min) / (max - min))


def make_ui(pipeline, im, tunes):
    app = QtWidgets.QApplication([])

    fig = fpl.Figure(shape=(1, 2))
    ax0, ax1 = fig[0, 0], fig[0, 1]
    orig = ax0.add_image(im)
    bin_artist = ax1.add_image((im > 0.5).astype(np.float32))
    ax0.title = "original"
    ax1.title = "thresholded"

    canvas = fig.show()

    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.addWidget(canvas)

    def update_image():
        r_im = pipeline(im)
        bin_artist.data = r_im.astype(np.float32)

    def update(v, tune, label):
        tune['value'] = _from_slider(v, tune['min'], tune['max'])
        label.setText(f"{tune['name']} : {tune['value']:.3f}")
        update_image()

    for tune_name, tune in tunes.items():
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(f"")
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)

        if tune['min'] is None:
            tune['min'] = 0.1 * tune['value']

        if tune['max'] is None:
            tune['max'] = 10 * tune

        slider.setRange(0, 100)
        slider.setValue(_to_slider(tune['value'], tune['min'], tune['max']))
        layout.addWidget(label)
        layout.addWidget(slider)
        lay.addLayout(layout)

        slider.valueChanged.connect(partial(update, tune=tune, label=label))
        update(_to_slider(tune['value'], tune['min'], tune['max']), tune, label)


    w.resize(1200, 600)
    w.show()
    app.exec()
