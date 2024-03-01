from random import randint, choice
import pygame

pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Игровое окно:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Содержит общие атрибуты объектов"""
    def __init__(self, body_color=None):
        """Инициализатор атрибутов"""
        self.position = CENTER_POSITION
        self.body_color = body_color

    def draw(self, surface):
        """Определяет, как объект будет отрисовываться на экране."""
        pass


class Apple(GameObject):
    """Описание яблока и его поведение."""
    def __init__(self, body_color=APPLE_COLOR, occupied_position=None):
        """Инициализирует атрибуты яблока."""
        super().__init__(body_color)
        if occupied_position is None:
            occupied_position = []
        self.randomize_position(occupied_position)

    def randomize_position(self, occupied_position):
        """Задает рандомные координаты яблока при столкновении со змейкой."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_position:
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание змейки и ее поведение."""
    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует атрибуты змейки."""
        super().__init__(body_color)
        self.head_position = self.position
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def update_direction(self):
        """Определение нового направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

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
        """При столкновении головы змейки с ее телом сбрасывает игру в начало."""
        if self.head_position in self.positions[1:]:
            self.length = 1
            self.positions = [self.position]
            screen.fill(BOARD_BACKGROUND_COLOR)
            self.next_direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object, length):
    """Задает направление змейки с помощью клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            for key in KEYS_DIRECTIONS:
                if length > 1:
                    if game_object.direction in key and event.key in key:
                        game_object.next_direction = KEYS_DIRECTIONS[key]
                elif event.key == key[0]:
                    game_object.next_direction = KEYS_DIRECTIONS[key]


def main():
    """Основная логика игры."""
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        apple.draw(screen)
        snake.draw(screen)
        handle_keys(snake, snake.length)
        snake.move()
        snake.get_head_position()
        snake.update_direction()
        snake.reset()
        pygame.display.update()

        if snake.head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
