def on_stereo_clicked(self):
    """
    Enables or disables stereo rendering based on the state of the stereo button.
    If stereo is enabled, sets the stereo "type" to CrystalEyes and enables the button to choose stereo parameters.
    If stereo is disabled, turns off stereo rendering and disables the button to choose stereo parameters.
    Updates the window after making the changes.
    """

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
    """
    Sets the inter-pupillary distance (IPD) for stereo rendering.

    Args:
        self: The instance of the class.
        ipd: The inter-pupillary distance value.

    Returns:
        None
    """

    # Get the active camera from the renderer
    camera = self.renderer.GetActiveCamera()

    # Set the inter-pupillary distance (IPD)
    camera.SetEyeSeparation(ipd)
    self.current_ipd = ipd
    # Update the window to apply the changes
    self.vtk_widget.GetRenderWindow().Render()
