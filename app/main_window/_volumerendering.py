import vtk


def on_volume_button_clicked(self):
    """
    Handle the event when the volume button is clicked.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    # Delete existing actor of the renderer
    self.renderer.RemoveAllViewProps()
    if self.ui.volume_button.isChecked():
        # If the button is checked: launch volume rendering of the selected organ
        selected_index = self.ui.organ_combo.currentIndex()
        self.segmented_actors = list(self.segmented_surface_actors)
        self.segmented_actors[selected_index] = self.segmented_volume_actors[
            selected_index
        ]
        # Disable the measurements' tab and enable histogram sliders
        self.ui.hist_group.setDisabled(False)
        self.ui.measure_tab.setDisabled(True)
    else:
        # If the button is unchecked: launch surface rendering
        self.segmented_actors = list(self.segmented_surface_actors)

        # Enable the measurements' tab and disable histogram sliders
        self.ui.hist_group.setDisabled(True)
        self.ui.measure_tab.setDisabled(False)

        for arrow, text in self.arrows:
            self.renderer.AddActor(arrow)
            self.renderer.AddActor(text)

        for actor in self.selected_cells:
            self.renderer.AddActor(actor)

        for actor in self.line_btw_cells:
            self.renderer.AddActor(actor)

    # Add the actors to the renderer
    for actor in self.segmented_actors:
        self.renderer.AddActor(actor)

    # Update window
    self.vtk_widget.GetRenderWindow().Render()


def on_volume_update(self):
    """
    Adjust the opacity of the selected organ's surface and volume actors based on user input.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    # Adjust opacity for a selected organ
    selected_index = self.ui.organ_combo.currentIndex()
    selected_surface_actor = self.segmented_surface_actors[selected_index]
    selected_volume_actor = self.segmented_volume_actors[selected_index]
    opacity = self.ui.op_slider.value() / 100

    # Set opacity for the surface actor
    selected_surface_actor.GetProperty().SetOpacity(opacity)

    # Set opacity for the surface actor
    selected_surface_actor.GetProperty().SetOpacity(opacity)

    # Set opacity for the volume actor
    opacity_func = vtk.vtkPiecewiseFunction()

    opacity_func.AddPoint(self.ui.low_slider.value(), 0)
    opacity_func.AddPoint(
        self.ui.high_slider.value(), self.ui.high_op_slider.value() / 100
    )
    selected_volume_actor.GetProperty().SetScalarOpacity(opacity_func)
    # Update window
    self.vtk_widget.GetRenderWindow().Render()
