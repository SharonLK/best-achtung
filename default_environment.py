import math

import gym
import numpy as np

from action import Action
from game import Game
from players.always_left_player import AlwaysLeftPlayer
from point import Point


class DefaultEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self) -> None:
        super().__init__()

        self.iterations = 0

        self.game = Game()
        self.other_bot = AlwaysLeftPlayer(self.game.head2)

        self.action_space = gym.spaces.Discrete(3)  # Turn left, Turn right, Continue straight
        # self.observation_space = gym.spaces.Box(low=0, high=2, shape=(200, 200))
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(7,))

    def _get_observation(self) -> np.ndarray:
        # resized = resize(self.game.surface, (200, 200), anti_aliasing=False)  #.astype(np.int8)
        # plt.figure()
        # plt.imshow(resized)
        # plt.show()

        distance_left = self.game.head1.pos[0]
        distance_right = self.game.width - self.game.head1.pos[0]
        distance_bottom = self.game.head1.pos[1]
        distance_top = self.game.height - self.game.head1.pos[1]

        position = Point(self.game.head1.x, self.game.head1.y)
        closest = 1131 ** 2
        closest1 = 1131 ** 2
        closest1_minus = 1131 ** 2
        closest_point0 = None
        closest_point_minus1 = None
        closest_point1 = None
        for point in self.game.head1.points[:-10] + self.game.obstacles_points + self.game.border_points:
            direction_to_point = math.degrees(math.atan2(point.y - position.y, point.x - position.x)) % 360
            actual_direction = math.degrees(self.game.head1.direction) % 360
            delta_direction = (direction_to_point - actual_direction) % 360
            # print(self.game.head1.direction % (math.pi * 2), direction_to_point % (math.pi * 2))
            # print(actual_direction)

            if delta_direction < 5 or delta_direction > 355:
                distance_squared = point.distance_squared(position)
                if distance_squared < closest:
                    closest = distance_squared
                    # closest_point = point

            if 5 <= delta_direction < 15:
                distance_squared = point.distance_squared(position)
                if distance_squared < closest1:
                    closest1 = distance_squared
                    # closest_point = point

            if 345 < delta_direction <= 355:
                distance_squared = point.distance_squared(position)
                if distance_squared < closest1_minus:
                    closest1_minus = distance_squared

        # return resized

        return np.array([
            # distance_left / self.game.width,
            # distance_right / self.game.width,
            # distance_bottom / self.game.width,
            # distance_top / self.game.width,
            math.sqrt(closest) / 1131,
            math.sqrt(closest1) / 1131,
            math.sqrt(closest1_minus) / 1131,
            self.game.head1.x / self.game.width,
            self.game.head1.y / self.game.width,
            (math.cos(self.game.head1.direction) + 1) / 2,
            (math.sin(self.game.head1.direction) + 1) / 2
        ])

        # return self.game.surface
        # return pygame.surfarray.array3d(pygame.display.get_surface()).astype(np.uint8)[:, :, 0]

    def step(self, action):
        if action == 0:
            action = Action.Right
        elif action == 1:
            action = Action.Left
        else:
            action = Action.Stand

        reward = 1

        self.game.advance(action, self.other_bot.move(self.game.board))
        self.iterations += 1

        distance_left = self.game.head1.pos[0]
        distance_right = self.game.width - self.game.head1.pos[0]
        distance_bottom = self.game.head1.pos[1]
        distance_top = self.game.height - self.game.head1.pos[1]

        # distance = min(distance_left, min(distance_right, min(distance_bottom, distance_top)))
        # if distance < 200:
        #     reward = -10

        observations = self._get_observation()
        ended = self.game.has_ended()

        # if ended and self.game.winner == 1:
        #     reward = 200
        # elif ended and self.game.winner == 2:
        #     reward = -200

        if ended:
            reward = -400

        # if self.iterations >= 250:
        #     ended = True
        #     reward = 50

        return observations, reward, int(ended), {}

    def reset(self) -> np.ndarray:
        # self.game.reset()
        # print('Restarting')
        self.game = Game()
        self.iterations = 0

        return self._get_observation()

    def render(self, mode='human') -> None:
        pass
