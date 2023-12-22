def on_opacity_changed(self):
    """Handles the change event of the opacity slider."""

    # Adjust opacity for a selected organ
    selected_index = self.ui.organ_combo.currentIndex()
    selected_surface_actor = self.segmented_surface_actors[selected_index]
    opacity = self.ui.op_slider.value() / 100

    # Set opacity for the surface actor
    selected_surface_actor.GetProperty().SetOpacity(opacity)

    # Set opacity for the surface actor
    selected_surface_actor.GetProperty().SetOpacity(opacity)

    # Update window
    self.vtk_widget.GetRenderWindow().Render()
