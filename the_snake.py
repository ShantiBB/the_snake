from random import randint, choice
import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
KEYS_DIRECTIONS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,

    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,

    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,

    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Содержит общие атрибуты объектов"""

    def __init__(self, body_color=None, position=CENTER_POSITION):
        """Инициализатор атрибутов"""
        self.position = position
        self.body_color = body_color

    def draw(self, surface, position):
        """Определяет, как объект будет отрисовываться на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Описание яблока и его поведение."""

    def __init__(self, body_color=APPLE_COLOR, occupied_position=()):
        """Инициализирует атрибуты яблока."""
        super().__init__(body_color)
        self.randomize_position(occupied_position)

    def randomize_position(self, occupied_position):
        """Задает рандомные координаты яблока при столкновении со змейкой."""
        while self.position in occupied_position:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )


class Snake(GameObject):
    """Описание змейки и ее поведение."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует атрибуты змейки."""
        super().__init__(body_color)
        self.head_position = self.position
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.length = 1

    def move(self):
        """Анимирование движения змейки."""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction
        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface, position):
        """Отрисовывает змейку на игровом поле."""
        super().draw(surface, position)
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Определяет голову змейки."""
        self.head_position = self.positions[0]

    def reset(self):
        """При столкновении головы змейки с ее телом
        сбрасывает игру в начало.
        """
        self.length = 1
        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object, length):
    """Задает направление змейки с помощью клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            for key in KEYS_DIRECTIONS:
                if length > 1:
                    if game_object.direction in key and event.key in key:
                        game_object.direction = KEYS_DIRECTIONS[key]
                elif event.key == key[0]:
                    game_object.direction = KEYS_DIRECTIONS[key]


def main():
    """Основная логика игры."""
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        snake.draw(screen, snake.positions[0])
        apple.draw(screen, apple.position)
        apple.randomize_position(snake.positions)
        handle_keys(snake, snake.length)
        snake.move()
        snake.get_head_position()
        pygame.display.update()

        if apple.position == snake.head_position:
            apple.randomize_position(snake.positions)
            snake.length += 1
        if snake.head_position in snake.positions[1:]:
            snake.reset()


if __name__ == '__main__':
    main()
