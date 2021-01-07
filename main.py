import time
import os
import sys
import pygame
import random

FPS = 144
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


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = HEIGHT


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)


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
    y = 0
    # создадим спрайт
    # добавим спрайт в группу
    n = 0
    mountain = Mountain()
    while running:
        if n == 0:
            start_screen()
        n = 1
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                y = 1
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Landing(event.pos)
        if y == 1:
            break
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(144)
    pygame.quit()
