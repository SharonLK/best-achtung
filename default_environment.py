import gym
import numpy as np
import pygame

from action import Action
from game import Game
from players.random_player import RandomPlayer


class DefaultEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self) -> None:
        super().__init__()

        self.game = Game()
        self.other_bot = RandomPlayer(self.game.head2)

        self.action_space = gym.spaces.Discrete(3)  # Turn left, Turn right, Continue straight
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(800, 600))

    def _get_observation(self) -> np.ndarray:
        return pygame.surfarray.array3d(pygame.display.get_surface()).astype(np.uint8)[:, :, 0]

    def step(self, action):
        if action == 0:
            action = Action.Right
        elif action == 1:
            action = Action.Left
        else:
            action = Action.Stand

        reward = 1

        self.game.advance(action, self.other_bot.move(self.game.board, keys=None))

        observations = self._get_observation()
        ended = self.game.has_ended()

        if ended and self.game.winner == 2:
            reward = 100
        elif ended and self.game.winner == 1:
            reward = -100

        return observations, reward, ended, {}

    def reset(self) -> np.ndarray:
        self.game.reset()

        return self._get_observation()

    def render(self, mode='human') -> None:
        pass
