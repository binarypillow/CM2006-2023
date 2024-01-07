from PyQt6.QtWidgets import QColorDialog
import vtk


def on_color_button(self):
    """
    Handles the click event of the colour button and sets the colour for the selected organ.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    color_dialog = QColorDialog(self)
    chosen_color = color_dialog.getColor()

    if chosen_color.isValid():
        selected_index = self.ui.organ_combo.currentIndex()
        selected_surface_actor = self.segmented_surface_actors[selected_index]
        selected_volume_actor = self.segmented_volume_actors[selected_index]
        rgb = chosen_color.redF(), chosen_color.greenF(), chosen_color.blueF()

        # Set colour for the surface actor
        selected_surface_actor.GetProperty().SetColor(rgb)

        # Set colour for the volume actor
        color_func = vtk.vtkColorTransferFunction()
        color_func.AddRGBPoint(0, 0, 0, 0)
        color_func.AddRGBPoint(255, *rgb)
        selected_volume_actor.GetProperty().SetColor(color_func)

        # Get the corresponding arrow actor
        selected_arrow_actor = self.arrows[selected_index][0]

        # Set the colour of the arrow actor to be the same as the surface actor
        selected_arrow_actor.GetProperty().SetColor(rgb)

        # Get the corresponding text actor
        selected_text_actor = self.arrows[selected_index][1]

        # Set the colour of the text actor to be the same as the surface actor
        selected_text_actor.GetProperty().SetColor(rgb)

        self.vtk_widget.GetRenderWindow().Render()

        # Update the colour of the button
        self.ui.color_button.setStyleSheet(
            f"border: 0px; background-color: rgb{tuple(int(c * 255) for c in rgb)}"
        )
        self.colors[selected_index] = rgb
