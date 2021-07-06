from typing import List

import numpy as np
import pygame

from constants import *
from game import Game
from players.human_player import HumanPlayer

clock = pygame.time.Clock()


def as_int(pos: np.ndarray) -> List[int]:
    return [int(pos[0]), int(pos[1])]


def main():
    play_music()
    pygame.init()
    game = Game()

    screen = pygame.display.set_mode(screen_size)

    player1 = HumanPlayer(game.head1, pygame.K_LEFT, pygame.K_RIGHT)
    player2 = HumanPlayer(game.head2, pygame.K_a, pygame.K_s)
    # player1 = RandomPlayer(game.head1)
    # player2 = Fogreedy(game.head2)
    empty = False

    while not game.has_ended():
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('game stopped by user request')
                game.end()

        keys = pygame.key.get_pressed()

        action1 = player1.move(game.board, keys)
        action2 = player2.move(game.board, keys)

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
    pygame.draw.circle(surface, color, center, RADIUS)


def draw_path(path, screen, color):
    for point in path:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], PATH_RADIUS)


def play_music():
    file = 'zot_ani.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


if __name__ == "__main__":
    main()
