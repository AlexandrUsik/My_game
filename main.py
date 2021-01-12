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
        self.rect.y = HEIGHT - 200
        self.x = 0
        self.y = 0
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect = self.rect.move(self.x,
                                   self.y)

    def move(self, x, y):
        self.x = x
        self.y = y
        if (self.rect.y + 200 >= HEIGHT) and (self.y > 1):
            print(self.rect.y + 200)
            print(HEIGHT)
            self.y = 0


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(300, 800, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
    hero = Hero(all_sprites)
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
                    hero.move(-5, 0)
                elif event.key == pygame.K_RIGHT:
                    hero.move(5, 0)
                elif event.key == pygame.K_UP:
                    hero.move(0, -5)
                elif event.key == pygame.K_DOWN:
                    hero.move(0, 5)
        if y == 1:
            break
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(144)
    pygame.quit()
