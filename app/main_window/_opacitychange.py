def on_opacity_changed(self):
    """
    Adjusts the opacity for a selected organ.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    # Adjust opacity for a selected organ
    selected_index = self.ui.organ_combo.currentIndex()
    selected_surface_actor = self.segmented_surface_actors[selected_index]
    opacity = self.ui.op_slider.value() / 100

    # Set opacity for the surface actor
    selected_surface_actor.GetProperty().SetOpacity(opacity)

    # Get the corresponding arrow actor
    selected_arrow_actor = self.arrows[selected_index][0]

    # Set the opacity of the arrow actor to be the same as the surface actor
    selected_arrow_actor.GetProperty().SetOpacity(opacity)

    # Get the corresponding text actor
    selected_text_actor = self.arrows[selected_index][1]

    # Set the opacity of the text actor to be the same as the surface actor
    selected_text_actor.GetProperty().SetOpacity(opacity)

    # Update window
    self.vtk_widget.GetRenderWindow().Render()
