# import gym
# import numpy as np
# from gym import spaces
#
# from board import Board
# from players.player import Player
#
#
# class Environment(gym.Env):
#     metadata = {'render.modes': ['human']}
#
#     def __init__(self, board: Board, player1: Player, player2: Player) -> None:
#         super(Environment, self).__init__()
#
#         self.board = board
#         self.my_player = player1
#         self.opponent = player2
#
#         self.action_space = spaces.Discrete(3)
#         self.observation_space = spaces.Tuple((
#             # my location
#             spaces.Box(low=0, high=self.board.width, shape=1),
#             spaces.Box(low=0, high=self.board.height, shape=1),
#             # opponent location
#             spaces.Box(low=0, high=self.board.width, shape=1),
#             spaces.Box(low=0, high=self.board.height, shape=1),
#             # board size
#             spaces.Box(low=0, high=board.width, shape=1),
#             spaces.Box(low=0, high=board.height, shape=1),
#             # board status
#             spaces.Box(low=0, high=1, shape=self.board.width*self.board.height, dtype=np.int32)
#         ))
#
#     def reset(self) -> np.ndarray:
#         self.board.reset()
#         return self._pull_observation()
#         return np.array([self.left_matka.y, self.right_matka.y, self.ball.x, self.ball.y, self.ball.speed])
#
#     def step(self, action):
#         if action == UP:
#             pass
