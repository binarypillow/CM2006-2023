from PyQt6.QtWidgets import QColorDialog
import vtk


def on_color_button_clicked(self):
    """Opens a color picker and sets the color of the selected actor based on the chosen color."""

    color_dialog = QColorDialog(self)
    chosen_color = color_dialog.getColor()

    if chosen_color.isValid():
        selected_index = self.ui.organ_combo.currentIndex()
        selected_surface_actor = self.segmented_surface_actors[selected_index]
        selected_volume_actor = self.segmented_volume_actors[selected_index]
        rgb = chosen_color.redF(), chosen_color.greenF(), chosen_color.blueF()

        # Set color for the surface actor
        selected_surface_actor.GetProperty().SetColor(rgb)

        # Set color for the volume actor
        color_func = vtk.vtkColorTransferFunction()
        color_func.AddRGBPoint(0, 0, 0, 0)
        color_func.AddRGBPoint(255, *rgb)
        selected_volume_actor.GetProperty().SetColor(color_func)

        self.vtk_widget.GetRenderWindow().Render()
        self.ui.color_button.setStyleSheet(
            f"border: 0px; background-color: rgb{tuple(int(c * 255) for c in rgb)}"
        )
        self.colors[selected_index] = rgb
