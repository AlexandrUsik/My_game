import time
import os
import sys
import pygame
import random

FPS = 60
WIDTH = 998
HEIGHT = 1200


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Impact.ttf', font_size=80):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    width = 376
    height = 113

    while True:
        button = Button(376, 113)
        button.draw(300, 395, game)

        button2 = Button2(376, 113)
        button2.draw(300, 620)

        button3 = Button3(376, 113)
        button3.draw(300, 879)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                return  # начинаем игру
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    (300 <= mouse[0] <= 300 + width) and (395 <= mouse[1] <= 395 + height):
                return
        pygame.display.flip()
        clock.tick(FPS)


def game():
    pygame.quit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (0, 138, 181)
        self.active_color = (0, 196, 255)
        self.end = 0

    def draw(self, x, y, action=None, font_size=80):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (x <= mouse[0] <= x + self.width) and (y <= mouse[1] <= y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1 and action is not None:
                action()
                self.end = 1

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        if self.end == 0:
            print_text('Start Game', x + 10, y + 10)


class Button2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (0, 138, 181)
        self.active_color = (0, 196, 255)

    def draw(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (x <= mouse[0] <= x + self.width) and (y <= mouse[1] <= y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text('Settings', x + 50, y + 10)


class Button3:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (0, 138, 181)
        self.active_color = (0, 196, 255)

    def draw(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (x <= mouse[0] <= x + self.width) and (y <= mouse[1] <= y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text('About', x + 90, y + 10)


class Hero(pygame.sprite.Sprite):
    image = load_image("stand.png")
    image = pygame.transform.scale(image, (100, 200))

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.direction = 'LEFT'
        self.stand = True
        self.rect.y = HEIGHT - 170
        self.x = 0
        self.y = 0
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if (self.rect.y + 200 >= HEIGHT + 30) and (self.y > 1):
            self.y = 0
        elif (self.rect.x + 100 >= WIDTH) and (self.x > 1):
            self.x = 0
        elif (self.rect.x <= 0) and (self.x < 1):
            self.x = 0
        self.rect = self.rect.move(self.x,
                                   self.y)
        self.gravity()
        if self.y == 0 and not self.stand:
            self.x = 0

    def move(self, x, y):
        self.was = self.x
        if x != -1:
            self.x = x
        if y != -1:
            self.y = y
            self.stand = False
        elif y == -1 and self.rect.y >= HEIGHT - 190:
            self.stand = True
        if (self.x > 0) and (self.was <= 0) and self.direction != 'RIGHT':
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = 'RIGHT'
        elif (self.x < 0) and (self.was >= 0) and self.direction != 'LEFT':
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = 'LEFT'

    def gravity(self):
        if self.y > 15 and self.y > 9 and self.rect.y >= HEIGHT - 190:
            self.y = -10
        elif self.y > -3 and self.y != 0:
            self.y += 0.5
        elif self.y < 0:
            self.y += 0.2


class Platform(pygame.sprite.Sprite):
    image = load_image("platform.png")
    max_x = WIDTH - 60
    max_y = HEIGHT - 50
    min_x = 10
    min_y = HEIGHT - 150
    list_of_min_y = []
    list_of_max_y = []

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if Platform.min_y not in Platform.list_of_min_y:
            Platform.list_of_min_y.append(Platform.min_y)
        else:
            Platform.min_y -= 100
        if Platform.max_y not in Platform.list_of_max_y:
            Platform.list_of_max_y.append(Platform.max_y)
        else:
            Platform.max_y -= 100
        self.rect.x = random.randint(Platform.min_x, Platform.max_x)
        self.rect.y = random.randint(Platform.min_y, Platform.max_y)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Свой курсор мыши')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    running = True
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    hero = pygame.sprite.Sprite()
    y = 0
    # создадим спрайт
    # добавим спрайт в группу
    n = 0
    button_up_down = 0
    hero = Hero(all_sprites)
    for _ in range(15):
        Platform(all_sprites)
    while running:
        if n == 0:
            start_screen()
        n = 1
        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image('fon_of_game.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                y = 1
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.move(-10, -1)
                elif event.key == pygame.K_RIGHT:
                    hero.move(10, -1)
                elif event.key == pygame.K_UP and button_up_down == 0:
                    hero.move(-1, -10)
                    button_up_down = 1
        if y == 1:
            break
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
