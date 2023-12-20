import numpy as np


class TimerCallback:
    def __init__(self, actors, index, camera):
        self.actors = actors
        self.timer_count = 0
        self.camera = camera
        self.index_organ = index
        self.initial_focal_point = camera.GetFocalPoint()
        self.center = self.actors[index].GetCenter()
        self.animation_running = True

    def execute(self, obj, event):
        if self.animation_running:

            self.initial_focal_point = self.camera.GetFocalPoint()

            # Moving vector to get closer to the correct focal point
            move_vector = [self.center[i] - self.initial_focal_point[i] for i in range(3)]

            # Compute new position : add a part of the moving vector
            new_focal_point = [self.initial_focal_point[i] + 0.1 * move_vector[i] for i in range(3)]
            self.camera.SetFocalPoint(new_focal_point)

            # Check if camera has the correct focal point
            if np.linalg.norm(np.array(self.center) - np.array(new_focal_point)) < 0.5:
                # Stop animation
                self.animation_running = False

            # Change opacity
            actors_to_change = self.actors[:self.index_organ] + self.actors[self.index_organ + 1:]
            for actor in actors_to_change:
                opacity_value = self.actors[self.index_organ].GetProperty().GetOpacity() - self.timer_count * 0.05
                if opacity_value > 0.05:
                    actor.GetProperty().SetOpacity(opacity_value)
                else:
                    actor.GetProperty().SetOpacity(0.05)
            self.actors[self.index_organ].GetProperty().SetOpacity(1)
            self.timer_count += 1

        obj.GetRenderWindow().Render()
