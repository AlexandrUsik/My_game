import os
import sys
import pygame
import random

FPS = 60
WIDTH = 998
HEIGHT = 1200


def print_text(message, x, y, font_color=(0, 0, 0), font_type='impact.ttf', font_size=80):
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


class Button_Of_Restart:
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

        print_text('Restart', WIDTH / 2 - 30, y + 12, (255, 255, 255), "impact.ttf", 20)


class Hero(pygame.sprite.Sprite):
    image = load_image("legs.png")
    image = pygame.transform.scale(image, (100, 200))

    jump_up = True
    y_of_hero = 0
    God_mod = 1
    jump_to_up = True

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH / 2

        self.direction = 'LEFT'
        self.mask = pygame.mask.from_surface(self.image)
        self.stand = True
        self.rect.y = HEIGHT - 170
        self.x = 0
        self.y = 0
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if Hero.God_mod != -1:
            if (self.rect.y + 200 >= HEIGHT + 30) and (self.y > 1):
                self.y = 0
                Hero.jump_up = False
            elif (self.rect.x + 100 >= WIDTH + 30) and (self.x > 1):
                self.rect.x = -30
            elif (self.rect.x <= -20) and (self.x < 1):
                self.rect.x = WIDTH - 20
            self.rect = self.rect.move(self.x,
                                       self.y)
            image_of_hero.filled(self.y, self.x, self.direction)
            self.gravity()
            if self.y == 0 and not self.stand:
                self.x = 0
            Hero.y_of_hero = self.rect.y
            if Hero.God_mod == 0 and Hero.y_of_hero >= 1010:
                Hero.God_mod = -1
        elif Hero.God_mod == -1:
            self.x = 0
            self.y = 0
            image_of_hero.filled(self.y, self.x, self.direction, self.rect.x, self.rect.y)

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
            Hero.jump_up = False
        elif self.y > -3 and self.y != 0:
            self.y += 0.6
            Hero.jump_up = True
        elif self.y < 0:
            self.y += 0.2
            Hero.jump_up = True
        if self.y > 7:
            Hero.jump_up = False
            self.y += 0.2
        if self.y <= 0:
            Hero.jump_to_up = True
        else:
            Hero.jump_to_up = False

    def broadcast(self, n):
        self.y = n


class Platform(pygame.sprite.Sprite):
    image = load_image("platform.png")
    min_y = 1050
    count_jj = 0
    count_of_jump = 0

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.down = 0
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - 100)
        self.rect.y = Platform.min_y
        Platform.min_y -= 100

    def update(self):
        if pygame.sprite.collide_mask(self, hero) and not Hero.jump_up:
            hero.broadcast(-10)
            Hero.God_mod = 0
            Platform.count_of_jump += 1
        if hero.y_of_hero < 600 and Hero.jump_to_up:
            Platform.count_jj = 5
        else:
            Platform.count_jj = 0
        if first_plat.rect.y > 1050:
            first_plat.rect.y = 150
        if second_plat.rect.y > 1050:
            second_plat.rect.y = 150
        if third_plat.rect.y > 1050:
            third_plat.rect.y = 150
        if fourth_plat.rect.y > 1050:
            fourth_plat.rect.y = 150
        if fifth_plat.rect.y > 1050:
            fifth_plat.rect.y = 150
        if six_plat.rect.y > 1050:
            six_plat.rect.y = 150
        if seven_plat.rect.y > 1050:
            seven_plat.rect.y = 150
        if eight_plat.rect.y > 1050:
            eight_plat.rect.y = 150
        if nine_plat.rect.y > 1050:
            nine_plat.rect.y = 150
        if ten_plat.rect.y > 1050:
            ten_plat.rect.y = 150
        self.rect = self.rect.move(0, Platform.count_jj)


class Imageof(pygame.sprite.Sprite):
    image = load_image("stand.png")
    image = pygame.transform.scale(image, (100, 200))

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Imageof.image
        self.rect = self.image.get_rect()

        self.gg_rect_x = 0
        self.gg_rect_y = 0

        self.rect.x = WIDTH / 2
        self.direction = 'LEFT'
        self.rect.y = HEIGHT - 170
        self.x = 0
        self.y = 0
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if Hero.God_mod != -1:
            if (self.rect.y + 200 >= HEIGHT + 30) and (self.y > 1):
                self.y = 0
                Hero.jump_up = False
            elif (self.rect.x + 100 >= WIDTH + 30) and (self.x > 1):
                self.rect.x = -30
            elif (self.rect.x <= -20) and (self.x < 1):
                self.rect.x = WIDTH - 20
            self.rect = self.rect.move(self.x,
                                       self.y)
            self.gg_rect_x = self.rect.x
            self.gg_rect_y = self.rect.y
        else:
            self.rect.x = self.gg_rect_x
            self.rect.y = self.gg_rect_y
            image_of_hero.image = load_image("death.png")
            if self.direction == 'RIGHT':
                image_of_hero.image = pygame.transform.scale(image_of_hero.image, (100, 200))
            else:
                image_of_hero.image = pygame.transform.scale(image_of_hero.image, (100, 200))
                image_of_hero.image = pygame.transform.flip(self.image, True, False)

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

    def filled(self, n, b, direction, rect_x=0, rect_y=0):
        self.y = n
        self.x = b
        self.direction = direction
        self.gg_rect_x = rect_x
        self.gg_rect_y = rect_y


class Endgame(pygame.sprite.Sprite):
    image = load_image("endgame.png")
    image = pygame.transform.scale(image, (300, 400))

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Endgame.image
        self.rect = self.image.get_rect()

        self.rect.x = 350
        self.direction = 'LEFT'
        self.rect.y = -400
        self.x = 0
        self.y = 0

    def update(self):
        if self.rect.y <= - 200:
            self.rect = self.rect.move(0,
                                       5)
        elif self.rect.y <= - 100:
            self.rect = self.rect.move(0,
                                       3)
        elif self.rect.y <= 0:
            self.rect = self.rect.move(0,
                                       2)
        elif self.rect.y <= 300:
            self.rect = self.rect.move(0,
                                       0)
            print_text('Количество прыжков', 410, 70, (255, 255, 255,), 'impact.ttf', 20)
            print_text(f'{Platform.count_of_jump}', 410, 110, (255, 255, 255,), 'impact.ttf', 20)
            button = Button_Of_Restart(100, 50)
            button.draw(WIDTH / 2 - 50, 300)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Свой курсор мыши')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    running = True
    all_sprites = pygame.sprite.Group()
    platforms_all = pygame.sprite.Group()
    endgame_sprite = pygame.sprite.Group()
    y = 0
    # создадим спрайт
    # добавим спрайт в группу
    n = 0
    button_up_down = 0
    sprite_of_end = 0

    hero = Hero(all_sprites)
    image_of_hero = Imageof(all_sprites)

    first_plat = Platform(platforms_all)
    second_plat = Platform(platforms_all)
    third_plat = Platform(platforms_all)
    fourth_plat = Platform(platforms_all)
    fifth_plat = Platform(platforms_all)
    six_plat = Platform(platforms_all)
    seven_plat = Platform(platforms_all)
    eight_plat = Platform(platforms_all)
    nine_plat = Platform(platforms_all)
    ten_plat = Platform(platforms_all)
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
                    image_of_hero.move(-10, -1)
                elif event.key == pygame.K_RIGHT:
                    hero.move(10, -1)
                    image_of_hero.move(10, -1)
                elif event.key == pygame.K_UP and button_up_down == 0:
                    hero.move(-1, -10)
                    button_up_down = 1
                    image_of_hero.move(-1, -10)
        if Hero.God_mod != -1:
            print_text(f'Count: {Platform.count_of_jump}', 10, 20, (255, 255, 255,), 'impact.ttf', 40)
        elif sprite_of_end == 0:
            endgame = Endgame(all_sprites)
            sprite_of_end = 1
        if y == 1:
            break
        if Hero.God_mod != -1:
            all_sprites.draw(screen)
            all_sprites.update()
            platforms_all.draw(screen)
            platforms_all.update()
        else:
            all_sprites.draw(screen)
            all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
