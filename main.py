from typing import List

import pygame
import numpy as np

from game import Game
from players.human_player import HumanPlayer
from players.random_palyer import RandomPlayer


radius = 5
path_radius = 5

screen_size = (5 * 240, 5 * 180)

p1_color = (255, 255, 255)
p2_color = (0, 255, 255)
p1_path_color = (255, 255, 0)
p2_path_color = (255, 0, 255)

BLACK = (0, 0, 0)


def as_int(pos: np.ndarray) -> List[int]:
    return [int(pos[0]), int(pos[1])]


def main():
    pygame.init()
    game = Game()

    screen = pygame.display.set_mode(screen_size)

    # player1 = HumanPlayer(game.head1, pygame.K_LEFT, pygame.K_RIGHT)
    # player2 = HumanPlayer(game.head1, pygame.K_q, pygame.K_w)
    player1 = RandomPlayer(game.head1)
    player2 = RandomPlayer(game.head2)
    empty = False

    while not game.has_ended():

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print('game stopped by user request')
                game.end()

        action1 = player1.move(game.board, events)
        action2 = player2.move(game.board, events)

        prev_pos1 = game.head1.pos
        prev_pos2 = game.head2.pos

        if empty:
            draw_player(BLACK, as_int(prev_pos1), screen)
            draw_player(BLACK, as_int(prev_pos2), screen)
        else:
            draw_player(p1_path_color, as_int(prev_pos2), screen)
            draw_player(p2_path_color, as_int(prev_pos2), screen)

        empty = game.advance(action1, action2)

        draw_player(p1_color, as_int(game.head1.pos), screen)
        draw_player(p2_color, as_int(game.head2.pos), screen)

        pygame.display.flip()


def draw_player(color, center, surface):
    pygame.draw.circle(surface, color, center, radius)


def draw_path(path, screen, color):
    for point in path:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], path_radius)


if __name__ == "__main__":
    main()
