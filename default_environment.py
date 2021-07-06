import gym
import numpy as np
import pygame

from action import Action
from game import Game


class DefaultEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self) -> None:
        super().__init__()

        self.game = Game(1)

        self.action_space = gym.spaces.Discrete(3)  # Turn left, Turn right, Continue straight
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(7,))

    def _get_observation(self) -> np.ndarray:
        risks = self.game.board.risks(self.game.heads[0])
        return np.ndarray([
            self.game.heads[0].pos[0] / self.game.board.width,
            self.game.heads[0].pos[1] / self.game.board.height,
            self.game.heads[0].direction / (2 * np.pi),
            risks[0],
            risks[1],
            risks[2],
            risks[3]
        ])

    def step(self, action):
        if action == 0:
            action = Action.Right
        elif action == 1:
            action = Action.Left
        else:
            action = Action.Stand

        self.game.advance(action)

        observations = self._get_observation()
        ended = self.game.has_ended()

        reward = self.game.time if self.game.has_ended() else 0

        return observations, reward, ended, {}

    def reset(self) -> np.ndarray:
        self.game.reset()

        return self._get_observation()

    def render(self, mode='human') -> None:
        pass
