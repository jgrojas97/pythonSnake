# JGR August 2024 - Simple Snake Game using PyGame module
import sys

import pygame
from pygame.locals import *
from random import randint

# initialize the pygame engine
pygame.init()

# screen and cell size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# background will be black, snake green and apple red
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# clock to control the frame rate
clock = pygame.time.Clock()
FPS = 10


class Snake:
    def __init__(self, color, screen_surface):
        self.color = color
        self.screen_surface = screen_surface
        self.direction = 0
        self.length = 1
        self.body = [(0, 0)]    # each body cell is 10px, reference is top left
        self.head = self.body[0]    # saving the coordinates of the head
        self.grow_tail = False

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        # the snake can only move in 4 directions, with the same speed
        y_disp = 0
        x_disp = 0
        # check direction and add displacement
        if self.direction == pygame.K_UP:
            y_disp = -CELL_SIZE
        elif self.direction == pygame.K_DOWN:
            y_disp = CELL_SIZE
        elif self.direction == pygame.K_RIGHT:
            x_disp = CELL_SIZE
        elif self.direction == pygame.K_LEFT:
            x_disp = -CELL_SIZE

        self.head = self.body[0]
        self.head = (self.head[0] + x_disp, self.head[1] + y_disp)
        self.body.insert(0, self.head)
        if self.grow_tail:
            self.grow_tail = False
        else:
            self.body.pop()

        if not self.detect_collision():
            self.draw()
            return True
        else:
            return False

    def draw(self):
        for body_x, body_y in self.body:
            pygame.draw.rect(self.screen_surface, self.color, pygame.Rect(body_x, body_y, CELL_SIZE, CELL_SIZE))

    def detect_collision(self):
        if self.head[0] < 0 or self.head[0] > SCREEN_WIDTH:
            return True
        if self.head[1] < 0 or self.head[1] > SCREEN_HEIGHT:
            return True
        if self.head in self.body[1:]:
            return True

    def grow(self):
        self.grow_tail = True


def main():
    # define any variable and create a snake object
    snake = Snake(GREEN, screen)
    game_is_running = True

    # first apple
    apple_position = (
    randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE, randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
    # main game loop
    pygame.event.clear()
    while game_is_running:
        # check output condition
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # print(event.key)
                snake.set_direction(event.key)
        # clean screen then send the screen object to the snake to draw itself
        screen.fill(BLACK)
        if not snake.move():
            game_is_running = False
        # check for apple:
        if snake.body[0] == apple_position:
            apple_position = (randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                              randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            snake.grow()
        # draw apple
        pygame.draw.rect(screen, RED, pygame.Rect(apple_position[0], apple_position[1], CELL_SIZE, CELL_SIZE))
        # update the screen at FPS
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
