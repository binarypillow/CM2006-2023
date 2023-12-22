from app.main_window.callback import TimerCallback


def on_glass_button_clicked(self):
    """Handles the click event of the glass button."""

    if self.ui.glass_button.isChecked():
        # The view changes
        selected_index = self.ui.organ_combo.currentIndex()

        timer_call = TimerCallback(
            self.segmented_actors, selected_index, self.renderer.GetActiveCamera()
        )
        self.interactor.AddObserver("TimerEvent", timer_call.execute)
        self.interactor.CreateRepeatingTimer(10)

        # Volume rendering possibility appears
        self.ui.hist_group.setDisabled(True)
        self.ui.volume_button.setDisabled(False)
        self.ui.organ_combo.setDisabled(True)
        self.ui.op_slider.setDisabled(True)
    else:
        # Volume rendering disappears and the volume becomes a surface
        self.ui.volume_button.setChecked(False)
        self.ui.volume_button.setDisabled(True)
        self.ui.organ_combo.setDisabled(False)
        self.ui.op_slider.setDisabled(False)
        self.on_volume_button_clicked()

        # The Focal point goes back to normal and all organs have an opacity of 1
        self.renderer.GetActiveCamera().SetFocalPoint(self.default_focal)
        for actor in self.segmented_actors:
            actor.GetProperty().SetOpacity(1)
