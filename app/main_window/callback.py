import numpy as np


class TimerCallback:
    """
    A callback class for executing animation and opacity changes on a set of actors.

    Args:
        actors (list): A list of vtkActor objects.
        index (int): The index of the organ to animate.
        camera (vtkCamera): The camera object.

    Returns:
        None
    """

    def __init__(self, actors, index, camera):
        self.actors = actors
        self.timer_count = 0
        self.camera = camera
        self.index_organ = index
        self.initial_focal_point = camera.GetFocalPoint()
        self.center = self.actors[index].GetCenter()
        self.animation_running = True

    def execute(self, obj, event):
        """
        Execute the animation and opacity changes based on the callback event.

        Args:
            self: The instance of the class.
            obj: The object that triggered the event.
            event: The event that was triggered.

        Returns:
            None
        """

        if self.animation_running:
            self.initial_focal_point = self.camera.GetFocalPoint()

            # Moving vector to get closer to the correct focal point
            move_vector = [
                self.center[i] - self.initial_focal_point[i] for i in range(3)
            ]

            # Compute new position: add a part of the moving vector
            new_focal_point = [
                self.initial_focal_point[i] + 0.1 * move_vector[i] for i in range(3)
            ]
            self.camera.SetFocalPoint(new_focal_point)

            # Check if camera has the correct focal point
            if np.linalg.norm(np.array(self.center) - np.array(new_focal_point)) < 0.5:
                # Stop animation
                self.animation_running = False

            # Change opacity
            actors_to_change = (
                self.actors[: self.index_organ] + self.actors[self.index_organ + 1 :]
            )
            for actor in actors_to_change:
                opacity_value = (
                    self.actors[self.index_organ].GetProperty().GetOpacity()
                    - self.timer_count * 0.05
                )
                if opacity_value > 0.05:
                    actor.GetProperty().SetOpacity(opacity_value)
                else:
                    actor.GetProperty().SetOpacity(0.05)
            self.actors[self.index_organ].GetProperty().SetOpacity(1)
            self.timer_count += 1

        obj.GetRenderWindow().Render()


class TimerChangeView:
    """
    A callback class for executing animation to change the view and roll of the camera.

    Args:
        target_view (list): The target view coordinates.
        target_roll (float): The target roll angle.
        camera (vtkCamera): The camera object.

    Returns:
        None
    """

    def __init__(self, target_view, target_roll, camera):
        self.target_view = target_view
        self.target_roll = target_roll
        self.camera = camera
        self.initial_position = camera.GetPosition()
        self.initial_roll = camera.GetRoll()
        self.animation_running = True
        self.continue_roll = True
        self.continue_position = True
        self.animation_step = 0.1
        self.tolerance = 0.5

    def execute(self, obj, event):
        """
        Execute the animation based on the callback event.

        Args:
            self: The instance of the class.
            obj: The object that triggered the event.
            event: The event that was triggered.

        Returns:
            None
        """

        if not self.animation_running:
            return
        new_roll = self.camera.GetRoll()
        new_position = self.camera.GetPosition()

        if self.continue_position:
            self.initial_position = self.camera.GetPosition()
            move_vector = [
                self.target_view[i] - self.initial_position[i] for i in range(3)
            ]
            new_position = [
                self.initial_position[i] + self.animation_step * move_vector[i]
                for i in range(3)
            ]
            self.camera.SetPosition(new_position)

            if (
                np.linalg.norm(np.array(self.target_view) - np.array(new_position))
                < self.tolerance
            ):
                self.continue_position = False

        if self.continue_roll:
            self.initial_roll = self.camera.GetRoll()
            move_roll = self.target_roll - self.initial_roll
            new_roll = self.initial_roll + self.animation_step * move_roll
            self.camera.SetRoll(new_roll)

            if np.abs(self.target_roll - new_roll) < self.tolerance:
                self.continue_roll = False

        if not self.continue_position and not self.continue_roll:
            self.animation_running = False

        obj.GetRenderWindow().Render()
