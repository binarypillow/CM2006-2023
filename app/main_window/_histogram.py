import numpy as np
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from app.utils import convert_to_gray_scale


def create_histogram(self, organs_data):
    """Creates a histogram plot for the selected organ data."""

    current_selected = self.ui.organ_combo.currentIndex()
    organ_data = convert_to_gray_scale(organs_data[current_selected])
    organ_data = organ_data[organ_data != 0]

    # Calculate the histogram data
    hist_data, bin_edges = np.histogram(organ_data, bins=256, range=(0, 256))
    canvas = FigureCanvas(Figure(figsize=(5, 3), dpi=100))

    ax = canvas.figure.subplots()
    # Create the histogram and get the bin values
    counts, bins, _ = ax.hist(
        hist_data,
        bins=128,
        range=[0, 256],
        density=False,
    )

    # Normalize the bin values
    counts_normalized = counts / np.sum(counts)

    # Clear the current figure
    ax.clear()

    # Plot the histogram with the normalized frequencies
    ax.bar(bins[:-1], counts_normalized, width=2, color="grey")

    # Define the coordinates of the four points of the polygon
    polygon_points = [
        (self.ui.low_slider.value(), 0),
        (self.ui.high_slider.value(), 0),
        (self.ui.high_slider.value(), self.ui.high_op_slider.value() / 100),
    ]
    # Create a Polygon object
    polygon = patches.Polygon(
        polygon_points,
        facecolor="lightgrey",
        alpha=0.5,
        linewidth=1.2,
        linestyle="--",
    )

    # Add the polygon to the current axes
    ax.add_patch(polygon)

    ax.set_ylim([0, 1])

    # Mark the vertices with gray dots
    for point in polygon_points:
        ax.scatter(*point, s=8, color="lightgrey", edgecolors="black")

    return canvas


def on_hist_slider_changed(self):
    """Updates the histogram canvas and slider constraints when the slider values change."""

    # Remove the old histogram canvas
    while self.ui.hist_layout.count():
        child = self.ui.hist_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    # Create a new histogram canvas with the updated vertical line position
    new_histogram_canvas = self.create_histogram(self.segmented_organs_data)

    # Add the new histogram canvas to the layout
    self.ui.hist_layout.addWidget(new_histogram_canvas)

    # Set constraints to avoid an invalid or empty interval
    self.ui.low_slider.setMaximum(self.ui.high_slider.value() - 1)
    self.ui.high_slider.setMinimum(self.ui.low_slider.value() + 1)
