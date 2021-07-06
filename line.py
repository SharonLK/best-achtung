import pygame
from math import sin, cos, pi
import numpy as np

speed = 0.15
dtheta = 0.3

radius = 5
path_radius = 5

screen_size = (5 * 240, 5 * 180)

p1_color = (255, 255, 255)
p2_color = (0, 255, 255)
p1_path_color = (255, 255, 0)
p2_path_color = (255, 0, 255)

BLACK = (0, 0, 0)


def choose_initial_pos():
    return np.random.uniform(low=0.25, high=0.75, size=2) * np.array(screen_size)


def choose_initial_angle(pos):
    if pos[0] < screen_size[0] / 2 and pos[1] < screen_size[1] / 2:
        angle = 0.25 * pi
    elif pos[0] < screen_size[0] / 2 and pos[1] > screen_size[1] / 2:
        angle = 0.75 * pi
    elif pos[0] > screen_size[0] / 2 and pos[1] > screen_size[1] / 2:
        angle = 1.25 * pi
    else:
        angle = 1.75 * pi

    return angle + pi * np.random.uniform(low=-0.25, high=0.25)


def distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    running = True

    cycle_time = 1000
    empty_time = 200

    p1_pos = choose_initial_pos()
    p2_pos = choose_initial_pos()
    while distance(p1_pos, p2_pos) < 250:
        p1_pos = choose_initial_pos()
        p2_pos = choose_initial_pos()

    p1_theta = choose_initial_angle(p1_pos)
    p2_theta = choose_initial_angle(p2_pos)

    p1_path = []
    p2_path = []

    time = 0

    while running:

        time += 1
        empty = time % cycle_time > cycle_time - empty_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    print('Quit game due to order')

                if event.key == pygame.K_LEFT:
                    p1_theta += dtheta
                if event.key == pygame.K_RIGHT:
                    p1_theta -= dtheta

                if event.key == pygame.K_q:
                    p2_theta += dtheta
                if event.key == pygame.K_w:
                    p2_theta -= dtheta

        if empty:
            draw_player(BLACK, [int(p1_pos[0]), int(p1_pos[1])], screen)
            draw_player(BLACK, [int(p2_pos[0]), int(p2_pos[1])], screen)
        else:
            draw_player(p1_path_color, [int(p1_pos[0]), int(p1_pos[1])], screen)
            draw_player(p2_path_color, [int(p2_pos[0]), int(p2_pos[1])], screen)

        p1_pos = update_pos(p1_theta, p1_pos)
        p2_pos = update_pos(p2_theta, p2_pos)

        draw_player(p1_color, [int(p1_pos[0]), int(p1_pos[1])], screen)
        draw_player(p2_color, [int(p2_pos[0]), int(p2_pos[1])], screen)

        pygame.display.flip()

        if check_border(p1_pos) or check_path_collision(p1_path, p2_path, p1_pos):
            print("player 1 lost")
            running = False
        elif check_border(p2_pos) or check_path_collision(p1_path, p2_path, p2_pos):
            print("player 2 lost")
            running = False

        if empty:
            p1_path = add_to_path(p1_path, p1_pos)
            p2_path = add_to_path(p2_path, p2_pos)


def draw_player(color, center, surface):
    pygame.draw.circle(surface, color, center, radius)


def draw_path(path, screen, color):
    for point in path:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], path_radius)


def update_pos(angle, pos):
    pos[0] += speed * sin(angle)
    pos[1] += speed * cos(angle)

    return pos


def add_to_path(path, pos):
    int_pos = [int(pos[0]), int(pos[1])]
    if int_pos not in path:
        path.append(int_pos)

    return path


def check_border(pos):
    if pos[0] + radius > screen_size[0] or pos[0] - radius < 0:
        return True
    elif pos[1] + radius > screen_size[1] or pos[1] - radius < 0:
        return True
    else:
        return False


def check_path_collision(path1, path2, pos):
    int_pos = [int(pos[0]), int(pos[1])]

    if int_pos in path1[:-2] or int_pos in path2[:-2]:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
