import pygame
import sys
import random


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current_position = self.get_head_position()
        x, y = self.direction
        new_position = ((current_position[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                        (current_position[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            snake_part = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, snake_part)
            pygame.draw.rect(surface, (93, 216, 228), snake_part, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            print(event.type == pygame.KEYDOWN)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        food = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, food)
        pygame.draw.rect(surface, (93, 216, 228), food, 1)


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    font = pygame.font.SysFont("monospace", 16)

    score = 0
    while (True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))

        text = font.render("Score {0}".format(score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))

        pygame.display.update()


main()
