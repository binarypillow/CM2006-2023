import vtk


def on_labels_button_clicked(self):
    """Toggle the visibility of arrow and text actors based on the state of the labels button."""

    if self.ui.labels_button.isChecked():
        for arrow, text in self.arrows:
            arrow.SetVisibility(True)
            text.SetVisibility(True)
    else:
        for arrow, text in self.arrows:
            arrow.SetVisibility(False)
            text.SetVisibility(False)
    # Update window
    self.vtk_widget.GetRenderWindow().Render()


def create_arrow_text(self):
    """Create arrow and text actors for each segmented surface actor."""

    labels = []
    for i in range(len(self.segmented_surface_actors)):
        # ARROW ACTOR
        arrow = vtk.vtkArrowSource()
        arrow.SetShaftRadius(0.05)
        arrow.SetTipRadius(0.1)
        arrow.SetTipLength(0.2)
        arrow.InvertOn()

        arrow_mapper = vtk.vtkPolyDataMapper()
        arrow_mapper.SetInputConnection(arrow.GetOutputPort())

        arrow_actor = vtk.vtkActor()
        arrow_actor.SetMapper(arrow_mapper)

        arrow_actor.RotateZ(180)  # Orient the arrow towards the centre

        actor = self.segmented_surface_actors[i]
        polydata = actor.GetMapper().GetInput()

        # Link the transparency of the arrow to the transparency of the surface
        arrow_actor.GetProperty().SetOpacity(actor.GetProperty().GetOpacity())
        arrow_actor.GetProperty().SetColor(actor.GetProperty().GetColor())

        # Get a cell from the polydata
        cell = polydata.GetCell(0)  # Get the first cell, adjust index as needed
        # Get the points of the cell
        points = cell.GetPoints()
        # Get the first point of the cell
        point = points.GetPoint(0)
        arrow_actor.SetPosition(point[0], point[1], point[2])

        # TEXT ACTOR
        text_source = vtk.vtkVectorText()
        text_source.SetText(self.ui.organ_combo.itemText(i))

        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(text_source.GetOutputPort())

        text_actor = vtk.vtkFollower()
        text_actor.SetMapper(text_mapper)

        # Link the transparency of the arrow to the transparency of the surface
        text_actor.GetProperty().SetOpacity(actor.GetProperty().GetOpacity())
        text_actor.GetProperty().SetColor(
            actor.GetProperty().GetColor()
        )  # Black color for text

        text_actor.SetPosition(point[0] + 200, point[1], point[2])
        text_actor.SetScale([6, 6, 6])
        arrow_actor.SetScale([30, 15, 15])

        arrow_actor.SetVisibility(False)
        text_actor.SetVisibility(False)
        labels.append([arrow_actor, text_actor])
    return labels


def update_arrow_and_text(self):
    """Update the position of arrow and text actors based on the segmented surface actors."""

    for i in range(len(self.segmented_surface_actors)):
        actor = self.segmented_surface_actors[i]
        polydata = actor.GetMapper().GetInput()

        # Get a cell from the polydata
        cell = polydata.GetCell(0)  # Get the first cell, adjust index as needed

        # Get the points of the cell
        points = cell.GetPoints()

        # Get the first point of the cell
        point = points.GetPoint(0)  # Get the first point, adjust index as needed

        # Update the position of the tip of the arrow
        self.arrows[i][0].SetPosition(point)

        # Update the position of the text actor behind the arrow
        text_actor_position = list(self.arrows[i][1].GetPosition())
        text_actor_position[0] = point[0] - 50
        self.arrows[i][1].SetPosition(text_actor_position)
        self.arrows[i][1].SetCamera(
            self.renderer.GetActiveCamera()
        )  # Set text orientation to face the camera


def on_camera_change(self, obj, event):
    """Callback function triggered when the camera changes."""
    self.update_arrow_and_text()
