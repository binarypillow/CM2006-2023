import vtk


def create_segmented_surface_actors(self):
    """Creates surface actors for segmented organs."""

    actors = []
    for organ in range(len(self.checked_labels)):
        # Filter data
        cast_filter = vtk.vtkImageCast()
        cast_filter.SetInputData(self.segmented_organs[organ])
        cast_filter.SetOutputScalarTypeToUnsignedShort()

        # Contour mapper : marching cubes
        contour = vtk.vtkMarchingCubes()
        contour.SetInputConnection(cast_filter.GetOutputPort())
        contour.ComputeNormalsOn()
        contour.ComputeGradientsOn()
        contour.SetValue(0, 60)

        con_mapper = vtk.vtkPolyDataMapper()
        con_mapper.SetInputConnection(contour.GetOutputPort())

        # Deactivate the scalar color to redefine a new color
        con_mapper.ScalarVisibilityOff()

        # Set up the surface actor
        surface_actor = vtk.vtkActor()
        surface_actor.SetMapper(con_mapper)

        # By default: one color per organ
        color = self.colors[organ % len(self.colors)]
        surface_actor.GetProperty().SetColor(color)

        surface_actor.GetProperty().SetOpacity(1.0)
        actors.append(surface_actor)

    return actors
