import gym
import numpy as np

from action import Action
from game import Game
from players.always_left_player import AlwaysLeftPlayer


class DefaultEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self) -> None:
        super().__init__()

        self.iterations = 0

        self.game = Game()
        self.other_bot = AlwaysLeftPlayer(self.game.head2)

        self.action_space = gym.spaces.Discrete(3)  # Turn left, Turn right, Continue straight
        # self.observation_space = gym.spaces.Box(low=0, high=2, shape=(200, 200))
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(4,))

    def _get_observation(self) -> np.ndarray:
        # resized = resize(self.game.surface, (200, 200), anti_aliasing=False)  #.astype(np.int8)
        # plt.figure()
        # plt.imshow(resized)
        # plt.show()

        distance_left = self.game.head1.pos[0]
        distance_right = self.game.width - self.game.head1.pos[0]
        distance_bottom = self.game.head1.pos[1]
        distance_top = self.game.height - self.game.head1.pos[1]

        # return resized

        return np.array([distance_left, distance_right, distance_bottom, distance_top]) / self.game.width

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

        distance = min(distance_left, min(distance_right, min(distance_bottom, distance_top)))
        if distance < 200:
            reward = -10

        observations = self._get_observation()
        ended = self.game.has_ended()

        if ended and self.game.winner == 1:
            reward = 200
        elif ended and self.game.winner == 2:
            reward = -200

        if self.iterations >= 250:
            ended = True
            reward = 50

        return observations, reward, int(ended), {}

    def reset(self) -> np.ndarray:
        # self.game.reset()
        # print('Restarting')
        self.game = Game()
        self.iterations = 0

        return self._get_observation()

    def render(self, mode='human') -> None:
        pass
