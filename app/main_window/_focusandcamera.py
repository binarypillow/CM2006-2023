from app.main_window.callback import TimerCallback, TimerChangeView


def on_glass_button_clicked(self):
    """
    Handles the click event of the glass button and performs actions based on its state.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    if self.ui.glass_button.isChecked():
        # The view changes
        selected_index = self.ui.organ_combo.currentIndex()

        timer_call = TimerCallback(
            self.segmented_actors, selected_index, self.renderer.GetActiveCamera()
        )
        self.interactor.AddObserver("TimerEvent", timer_call.execute)
        self.interactor.CreateRepeatingTimer(10)

        # Enable the volume rendering button and disable opacity slider and combobox
        self.ui.hist_group.setDisabled(True)
        self.ui.volume_button.setDisabled(False)
        self.ui.organ_combo.setDisabled(True)
        self.ui.op_slider.setDisabled(True)
    else:
        # Disable the volume rendering button and enable opacity slider and combobox
        self.ui.volume_button.setChecked(False)
        self.ui.volume_button.setDisabled(True)
        self.ui.organ_combo.setDisabled(False)
        self.ui.op_slider.setDisabled(False)
        self.on_volume_button_clicked()

        # The Focal point goes back to normal, and all organs have an opacity of 1
        self.renderer.GetActiveCamera().SetFocalPoint(self.default_focal)
        for actor in self.segmented_actors:
            actor.GetProperty().SetOpacity(1)


def on_action_view(self):
    """
    Handles the view actions and changes the camera position and roll accordingly.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    action = self.sender()  # Get the action that emits the signal

    # Get the action text
    action_text = action.text()
    roll = 110
    position = [-0.68699, -371.3468, 61.26843]

    if action_text == "Front view":
        roll = 110
        position = [-0.68699, -371.3468, 61.26843]

    elif action_text == "Back view":
        roll = -110
        position = [697.2861264037024, 754.3462833804862, 335.8932959471566]

    elif action_text == "Left view":
        roll = 122
        position = [-252.7331129670938, 528.9943727080589, 282.7663873549244]

    elif action_text == "Right view":
        roll = -122
        position = [704.8874040430634, -87.79915520628937, 7.8853664987301]

    timer_view = TimerChangeView(position, roll, self.renderer.GetActiveCamera())
    self.interactor.AddObserver("TimerEvent", timer_view.execute)
    self.interactor.CreateRepeatingTimer(10)


def reset_view(self):
    """
    Resets the view of the camera to its initial position, roll, and focal point.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    self.renderer.GetActiveCamera().SetPosition(self.initial_camera_position)
    self.renderer.GetActiveCamera().SetRoll(self.initial_camera_roll)
    self.renderer.GetActiveCamera().SetFocalPoint(self.initial_camera_focal_point)
    self.vtk_widget.GetRenderWindow().Render()
