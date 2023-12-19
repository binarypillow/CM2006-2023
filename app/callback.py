import numpy as np


class TimerCallback:
    def __init__(self, actors, index):
        self.actors = actors
        self.center_actor = self.actors[index]
        self.timer_count = 0
        self.animation_running = True

    def execute(self, obj, event):
        if self.animation_running:

            initial_position_specified = self.center_actor.GetPosition()

            actor_bounds = self.center_actor.GetBounds()

            # Compute the center of the actor
            actor_center_x = (actor_bounds[0] + actor_bounds[1]) / 2.0
            actor_center_y = (actor_bounds[2] + actor_bounds[3]) / 2.0
            actor_center_z = (actor_bounds[4] + actor_bounds[5]) / 2.0

            new_position = (-actor_center_x, -actor_center_y, -actor_center_z)

            # Moving vector of specified actor
            move_vector = [new_position[i] - initial_position_specified[i] for i in range(3)]

            for other_actor in self.actors:
                # Get initial position of the actor
                initial_position_other = other_actor.GetPosition()

                # Compute new position : add a part of the moving vector
                new_position_other = [initial_position_other[i] + 0.1 * move_vector[i] for i in range(3)]

                # Define position
                other_actor.SetPosition(new_position_other)

            # Check if actor has the correct position
            current_position_specified = self.center_actor.GetPosition()
            print(current_position_specified, new_position)
            if np.linalg.norm(np.array(current_position_specified) - np.array(new_position)) < 10:
                # Stop animation
                self.animation_running = False
            self.timer_count += 1

        obj.GetRenderWindow().Render()
