import numpy as np
import fastplotlib as fpl
from PySide6 import QtWidgets, QtCore
from functools import partial

from .helper_functions import find_in_args_or_kwargs, replace_in_args_or_kwargs, resolve_argname, add_written_names


def _from_slider(val, min, max):
    return min + val / 1000.0 * (max - min)


def _to_slider(val, min, max):
    return int(1000.0 * (val - min) / (max - min))


def _build_ui_widget(pipeline, im, tunes):
    add_written_names(tunes)

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

    def update(v, tune, label, arg_index):
        use_argnames = tune['argnames'] is not None
        argnum = tune['argnums'][arg_index] if not use_argnames else None
        argname = tune['argnames'][arg_index] if use_argnames else None

        v = _from_slider(v, tune['min'], tune['max'])
        replace_in_args_or_kwargs(tune['argspec'], tune['args'], tune['kwargs'], v,
                                  argnum=argnum, argname=argname)

        argname = resolve_argname(tune['argspec'], argnum=argnum, argname=argname)
        label.setText(f"{tune['index'] + 1} : {tune['written_name']} ({argname}): {v:.3f}")

        update_image(tune)

    for tune in tunes.values():
        use_argnames = tune['argnames'] is not None
        n_tunable = len(tune['argnames']) if use_argnames else len(tune['argnums'])

        for arg_index in range(n_tunable):
            layout = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel("")
            slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)

            if use_argnames:
                value = find_in_args_or_kwargs(tune['argspec'], tune['args'], tune['kwargs'],
                                               argname=tune['argnames'][arg_index])
            else:
                value = find_in_args_or_kwargs(tune['argspec'], tune['args'], tune['kwargs'],
                                               argnum=tune['argnums'][arg_index])

            if tune['min'] is None:
                tune['min'] = 0.1 * value

            if tune['max'] is None:
                tune['max'] = 10 * value

            slider.setRange(0, 1000)
            slider.setValue(_to_slider(value, tune['min'], tune['max']))
            layout.addWidget(label)
            layout.addWidget(slider)
            lay.addLayout(layout)

            slider.valueChanged.connect(partial(update, tune=tune, label=label, arg_index=arg_index))
            v = _to_slider(value, tune['min'], tune['max'])
            slider.sliderPressed.connect(partial(update, v=v, tune=tune, label=label, arg_index=arg_index))
            update(v=v, tune=tune, label=label, arg_index=arg_index)

    return w

def make_ui(pipeline, im, tunes, width=1200, height=600):
    app = QtWidgets.QApplication([])
    w = _build_ui_widget(pipeline, im, tunes)
    w.resize(width, height)
    w.show()
    app.exec()

