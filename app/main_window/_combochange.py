import vtk


def on_combo_box_changed(self):
    """Handles the change event of the combo box."""

    # Change organ
    selected_index = self.ui.organ_combo.currentIndex()
    selected_actor = self.segmented_actors[selected_index]

    if isinstance(selected_actor, vtk.vtkActor):
        opacity = selected_actor.GetProperty().GetOpacity()
        self.ui.op_slider.setValue(int(opacity * 100))

    # Update the active color widget with the color of the selected organ
    rgb = tuple(int(c * 255) for c in self.colors[selected_index % len(self.colors)])
    self.ui.color_button.setStyleSheet(f"border: 0px; background-color: rgb{rgb};")

    # Update the histogram
    new_histogram_canvas = self.create_histogram(self.segmented_organs_data)

    # Remove the old histogram canvas
    while self.ui.hist_layout.count():
        child = self.ui.hist_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    # Add the new histogram canvas to the layout
    self.ui.hist_layout.addWidget(new_histogram_canvas)
    self.ui.low_slider.setValue(0)
    self.ui.high_slider.setValue(255)
    self.ui.high_op_slider.setValue(100)

    # Update volume and surface values
    area, volume = self.calculate_surface_volume()

    self.ui.surface_value.setText(f"{area:,.2f} mm²")
    self.ui.volume_value.setText(f"{volume:,.2f} mm³")
