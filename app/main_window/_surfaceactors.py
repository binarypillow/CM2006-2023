import vtk


def create_segmented_surface_actors(self):
    """
    Create segmented surface actors for each checked label.

    Args:
        self: The instance of the class.

    Returns:
        list: A list of vtkActor objects representing the segmented surface actors.
    """

    actors = []
    for organ in range(len(self.checked_labels)):
        # Filter data
        cast_filter = vtk.vtkImageCast()
        cast_filter.SetInputData(self.segmented_organs[organ])
        cast_filter.SetOutputScalarTypeToUnsignedShort()

        # Contour mapper: marching cubes
        contour = vtk.vtkMarchingCubes()
        contour.SetInputConnection(cast_filter.GetOutputPort())
        contour.ComputeNormalsOn()
        contour.ComputeGradientsOn()
        contour.SetValue(0, 60)

        con_mapper = vtk.vtkPolyDataMapper()
        con_mapper.SetInputConnection(contour.GetOutputPort())

        # Deactivate the scalar colour to redefine a new colour
        con_mapper.ScalarVisibilityOff()

        # Set up the surface actor
        surface_actor = vtk.vtkActor()
        surface_actor.SetMapper(con_mapper)

        # By default: one colour per organ
        color = self.colors[organ % len(self.colors)]
        surface_actor.GetProperty().SetColor(color)

        surface_actor.GetProperty().SetOpacity(1.0)
        actors.append(surface_actor)

    return actors
