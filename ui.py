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

    intermediate_plot = len(tunes) > 1

    fig = fpl.Figure(shape=(1, 3 if intermediate_plot else 2))
    if intermediate_plot:
        ax_orig, ax_intermediate, ax_final = fig[0, 0], fig[0, 1], fig[0, 2]
        ax_intermediate.title = "intermediate"
        bin_intermediate = ax_intermediate.add_image(im)
    else:
        ax_orig, ax_intermediate, ax_final = fig[0, 0], None, fig[0, 1]

    bin_orig = ax_orig.add_image(im)
    bin_final = ax_final.add_image(im)

    ax_orig.title = "original"
    ax_final.title = "final"

    canvas = fig.show()

    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.addWidget(canvas)

    def update_image(tune):
        r_im = pipeline(im)
        bin_final.data = r_im.astype(np.float32)
        if intermediate_plot:
            bin_intermediate.data = tune['result'].astype(np.float32)
            ax_intermediate.title = f'{tune['index'] + 1} : {tune['written_name']}'

    def update(v, tune, label):
        tune['value'] = _from_slider(v, tune['min'], tune['max'])
        label.setText(f"{tune['index'] + 1} : {tune['written_name']} : {tune['value']:.3f}")
        update_image(tune)

    for (tune_name, tune_idx), tune in tunes.items():
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(f"")
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)

        if tune['min'] is None:
            tune['min'] = 0.1 * tune['value']

        if tune['max'] is None:
            tune['max'] = 10 * tune['value']

        slider.setRange(0, 100)
        slider.setValue(_to_slider(tune['value'], tune['min'], tune['max']))
        layout.addWidget(label)
        layout.addWidget(slider)
        lay.addLayout(layout)

        slider.valueChanged.connect(partial(update, tune=tune, label=label))
        v = _to_slider(tune['value'], tune['min'], tune['max'])
        slider.sliderPressed.connect(partial(update, v=v, tune=tune, label=label))
        update(v, tune, label)


    w.resize(1200, 600)
    w.show()
    app.exec()
