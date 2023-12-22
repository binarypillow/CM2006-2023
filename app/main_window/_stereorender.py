def on_stereo_clicked(self):
    """Handles the click event of the stereo button."""

    if self.ui.stereo_button.isChecked():
        self.vtk_widget.GetRenderWindow().SetStereoTypeToCrystalEyes()
        self.vtk_widget.GetRenderWindow().StereoRenderOn()
        # Enable button to choose stereo parameters
        self.ui.stereo_param_button.setDisabled(False)

    else:
        self.vtk_widget.GetRenderWindow().StereoRenderOff()
        self.ui.stereo_param_button.setDisabled(True)

    # Update window
    self.vtk_widget.GetRenderWindow().Render()


def set_stereo_values(self, ipd):
    """Sets the inter-pupillary distance (IPD) for stereo rendering."""

    # Get the active camera from the renderer
    camera = self.renderer.GetActiveCamera()

    # Set the inter-pupillary distance (IPD) in degree
    camera.SetEyeAngle(ipd)
    self.current_ipd = ipd
    # Update the window to apply the changes
    self.vtk_widget.GetRenderWindow().Render()
