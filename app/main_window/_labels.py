import vtk


def on_labels_button_clicked(self):
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
    labels = []
    for i in range(len(self.segmented_surface_actors)):
        arrow = vtk.vtkArrowSource()
        arrow.SetShaftRadius(0.07)
        arrow.SetTipRadius(0.3)
        arrow.SetTipLength(0.3)

        arrow_mapper = vtk.vtkPolyDataMapper()
        arrow_mapper.SetInputConnection(arrow.GetOutputPort())

        arrow_actor = vtk.vtkActor()
        arrow_actor.SetMapper(arrow_mapper)

        text_source = vtk.vtkVectorText()
        text_source.SetText(self.ui.organ_combo.itemText(i))

        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(text_source.GetOutputPort())

        text_actor = vtk.vtkFollower()
        text_actor.SetMapper(text_mapper)
        text_actor.GetProperty().SetColor(0, 0, 0)  # Black color for text

        center = self.segmented_surface_actors[i].GetCenter()

        arrow_actor.SetPosition(center)
        arrow_actor.RotateZ(180)  # Orient the arrow towards the center
        #arrow_actor.RotateWXYZ(90, 0, 1, 0)  # Correct orientation (adjust angles if needed)

        text_actor.SetPosition(center[0] + 50, center[1], center[2])
        arrow_actor.SetPosition(center[0] + 50, center[1], center[2])
        text_actor.SetScale([6, 6, 6])
        arrow_actor.SetScale([30, 15, 15])

        arrow_actor.SetVisibility(False)
        text_actor.SetVisibility(False)
        labels.append([arrow_actor, text_actor])
    return labels


def update_arrow_and_text(self):
    for i in range(len(self.segmented_surface_actors)):
        # actor_position = self.segmented_surface_actors[i].GetCenter()
        # arrow_position = [actor_position[0] - 2, actor_position[1], actor_position[2]]
        # self.arrows[i][0].SetPosition(arrow_position)

        # text_actor_position = list(self.arrows[i][1].GetPosition())
        # text_actor_position[0] = actor_position[0] - 2
        # self.arrows[i][1].SetPosition(text_actor_position)
        self.arrows[i][1].SetCamera(self.renderer.GetActiveCamera())  # Set text orientation to face the camera


def on_camera_change(self, obj, event):
    self.update_arrow_and_text()
