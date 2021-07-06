from math import cos, pi, sin

import numpy as np
import pygame

speed = 0.15
dtheta = 0.3

radius = 5
path_radius = 5

# screen_size = (5 * 240, 5 * 180)
screen_size = (800, 600)

p1_color = (255, 255, 255)
p2_color = (0, 255, 255)
p1_path_color = (255, 255, 0)
p2_path_color = (255, 0, 255)

BLACK = (0, 0, 0)


class Simulator:
    def __init__(self) -> None:
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)

        self.p1_pos = self.choose_initial_pos()
        self.p2_pos = self.choose_initial_pos()
        while self.distance(self.p1_pos, self.p2_pos) < 250:
            self.p1_pos = self.choose_initial_pos()
            self.p2_pos = self.choose_initial_pos()

        self.p1_theta = self.choose_initial_angle(self.p1_pos)
        self.p2_theta = self.choose_initial_angle(self.p2_pos)

        self.p1_path = []
        self.p2_path = []

        self.running = True
        self.time = 0

    def choose_initial_pos(self):
        return np.random.uniform(low=0.25, high=0.75, size=2) * np.array(screen_size)

    def choose_initial_angle(self, pos):
        if pos[0] < screen_size[0] / 2 and pos[1] < screen_size[1] / 2:
            angle = 0.25 * pi
        elif pos[0] < screen_size[0] / 2 and pos[1] > screen_size[1] / 2:
            angle = 0.75 * pi
        elif pos[0] > screen_size[0] / 2 and pos[1] > screen_size[1] / 2:
            angle = 1.25 * pi
        else:
            angle = 1.75 * pi

        return angle + pi * np.random.uniform(low=-0.25, high=0.25)

    def distance(self, pos1, pos2):
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def draw_player(self, color, center, surface):
        pygame.draw.circle(surface, color, center, radius)

    def draw_path(self, path, screen, color):
        for point in path:
            pygame.draw.circle(screen, color, [int(point[0]), int(point[1])], path_radius)

    def update_pos(self, angle, pos):
        pos[0] += speed * sin(angle) * 50
        pos[1] += speed * cos(angle) * 50

        return pos

    def add_to_path(self, path, pos):
        int_pos = [int(pos[0]), int(pos[1])]
        if int_pos not in path:
            path.append(int_pos)

        return path

    def check_border(self, pos):
        if pos[0] + radius > screen_size[0] or pos[0] - radius < 0:
            return True
        elif pos[1] + radius > screen_size[1] or pos[1] - radius < 0:
            return True
        else:
            return False

    def check_path_collision(self, path1, path2, pos):
        int_pos = [int(pos[0]), int(pos[1])]

        if int_pos in path1[:-2] or int_pos in path2[:-2]:
            return True
        else:
            return False

    def step(self):
        cycle_time = 1000
        empty_time = 200

        self.time += 1
        empty = self.time % cycle_time > cycle_time - empty_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    print('Quit game due to order')

                if event.key == pygame.K_LEFT:
                    self.p1_theta += dtheta
                if event.key == pygame.K_RIGHT:
                    self.p1_theta -= dtheta

                if event.key == pygame.K_q:
                    self.p2_theta += dtheta
                if event.key == pygame.K_w:
                    self.p2_theta -= dtheta

        if empty:
            self.draw_player(BLACK, [int(self.p1_pos[0]), int(self.p1_pos[1])], self.screen)
            self.draw_player(BLACK, [int(self.p2_pos[0]), int(self.p2_pos[1])], self.screen)
        else:
            self.draw_player(p1_path_color, [int(self.p1_pos[0]), int(self.p1_pos[1])], self.screen)
            self.draw_player(p2_path_color, [int(self.p2_pos[0]), int(self.p2_pos[1])], self.screen)

        p1_pos = self.update_pos(self.p1_theta, self.p1_pos)
        p2_pos = self.update_pos(self.p2_theta, self.p2_pos)

        self.draw_player(p1_color, [int(p1_pos[0]), int(p1_pos[1])], self.screen)
        self.draw_player(p2_color, [int(p2_pos[0]), int(p2_pos[1])], self.screen)

        pygame.display.flip()

        if self.check_border(p1_pos) or self.check_path_collision(self.p1_path, self.p2_path, p1_pos):
            print("player 1 lost")
            self.running = False
        elif self.check_border(p2_pos) or self.check_path_collision(self.p1_path, self.p2_path, p2_pos):
            print("player 2 lost")
            self.running = False

        if empty:
            p1_path = self.add_to_path(self.p1_path, p1_pos)
            p2_path = self.add_to_path(self.p2_path, p2_pos)

    def has_ended(self):
        return not self.running


if __name__ == "__main__":
    running = True

    simulator = Simulator()
    while running:
        simulator.step()
