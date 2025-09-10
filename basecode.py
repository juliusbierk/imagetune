import numpy as np
from skimage import data, color, exposure, filters
import fastplotlib as fpl
from PySide6 import QtWidgets, QtCore

app = QtWidgets.QApplication([])

img = color.rgb2gray(data.astronaut())
img = exposure.rescale_intensity(img, in_range='image', out_range=(0.0, 1.0))

fig = fpl.Figure(shape=(1, 2))
ax0, ax1 = fig[0, 0], fig[0, 1]
orig = ax0.add_image(img)
bin_artist = ax1.add_image((img > 0.5).astype(np.float32))
ax0.title = "original"
ax1.title = "thresholded"

canvas = fig.show()

w = QtWidgets.QWidget()
lay = QtWidgets.QVBoxLayout(w)
lay.addWidget(canvas)

# --- Threshold slider with label ---
thresh_layout = QtWidgets.QHBoxLayout()
thresh_label = QtWidgets.QLabel("Threshold: 0.50")
slider_thresh = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
slider_thresh.setRange(0, 100)
slider_thresh.setValue(50)
thresh_layout.addWidget(thresh_label)
thresh_layout.addWidget(slider_thresh)
lay.addLayout(thresh_layout)

# --- Blur slider with label ---
blur_layout = QtWidgets.QHBoxLayout()
blur_label = QtWidgets.QLabel("Blur (σ): 0.0")
slider_blur = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
slider_blur.setRange(0, 20)   # corresponds to sigma=0..2.0
slider_blur.setValue(0)
blur_layout.addWidget(blur_label)
blur_layout.addWidget(slider_blur)
lay.addLayout(blur_layout)

state = {
    "threshold": 0.5,
    "sigma": 0.0,
}

def update_image():
    blurred = filters.gaussian(img, sigma=state["sigma"]) if state["sigma"] > 0 else img
    bin_artist.data = (blurred > state["threshold"]).astype(np.float32)

def update_thresh(v):
    state["threshold"] = v / 100.0
    thresh_label.setText(f"Threshold: {state['threshold']:.2f}")
    update_image()

def update_blur(v):
    state["sigma"] = v / 10.0   # slider 0..20 → sigma 0..2.0
    blur_label.setText(f"Blur (σ): {state['sigma']:.1f}")
    update_image()

slider_thresh.valueChanged.connect(update_thresh)
slider_blur.valueChanged.connect(update_blur)

w.resize(1200, 600)
w.show()
app.exec()
