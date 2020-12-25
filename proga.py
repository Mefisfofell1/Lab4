import pygame
import os
import random

fps = 3000
pygame.init()
speed = 2
Clock = 0
clock = pygame.time.Clock()
gaming = True
point = 0
black = (0, 0, 0)
lifes = 5

#pygame.mixer.music.load('music.wav')

#pygame.mixer.music.play()


def draw2(lifes):
    font = pygame.font.Font('aerial.ttf', 50)
    text = font.render(str(lifes), 1, (0, 0, 255))
    text_x = 700
    text_y = 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))


def draw(point):
    screen.fill((0, 0, 0))
    font = pygame.font.Font('aerial.ttf', 50)
    text = font.render(str(point), 1, (0, 0, 255))
    text_x = 20
    text_y = 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def terminate():
    pygame.quit()


def points(point):
    point += 1


def gameoverScreen(point):
    introText = ["Gameover", "",
                 'Points:', str(point)]

    screen.fill(pygame.Color('black'))
    font = pygame.font.Font('aerial.ttf', 30)
    textCoord = 50
    for line in introText:
        stringRendered = font.render(line, 1, pygame.Color('white'))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 10
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                gaming = True
                return gaming
        pygame.display.flip()
        clock.tick(fps)


class Hostile(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('Enemy.png'), (50, 30))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Hostile.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect = self.rect.move(-1, 0)


class Pulya(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('KAMAPYLA.png'), (5, 5))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Pulya.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect = self.rect.move(-1, 0)


class Border(pygame.sprite.Sprite):

    def __init__(self, x1, y1, x2, y2, vertical_borders, horizontal_borders):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('KAMAPYLA.png'), (5, 5))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect = self.rect.move(10, 0)


class Sprite(pygame.sprite.Sprite):
    image = load_image("monkas.png")

    def __init__(self, group):

        super().__init__(group)

        self.image = Sprite.image
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = 220

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.rect.y -= 30

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.rect.y += 30


def spawn(point):
    global Clock
    raising_point = point
    spawning_number = 5
    if raising_point >= 10:
        spawning_number += 1
        raising_point = 0
    Clock += 1
    if Clock > 300:
        for i in range(spawning_number):
            Hostile(all_hostiles, 800, random.randint(20, 580))
        Clock = 0


def out_of_range(border, all_bullets):
    pygame.sprite.spritecollide(border, all_bullets, True)


def kill(all_hostiles, all_bullets):
    global point

    for bullet in all_bullets:
        if pygame.sprite.spritecollideany(bullet, all_hostiles):
            point += 1

        pygame.sprite.spritecollide(bullet, all_hostiles, True)


def lose(losing_border, all_hostiles):
    global lifes
    global gaming

    if pygame.sprite.spritecollideany(losing_border, all_hostiles):
        pygame.sprite.spritecollide(losing_border, all_hostiles, True)
        lifes -= 1


all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_hostiles = pygame.sprite.Group()

vertical_borders = pygame.sprite.Group()

sprite = pygame.sprite.Sprite()
sprite.image = load_image("monkas.png")
sprite.rect = sprite.image.get_rect()
hero_image = pygame.transform.scale(load_image('monkas.png'), (50, 30))
hero1 = Sprite(all_sprites)
hero1.image = hero_image
hero1.rect = hero1.image.get_rect()
hero1.rect.x = 0
hero1.rect.y = 0

display = pygame.display.set_mode((800, 600))
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
running = True

losing_border = Border(5, 5, 5, height - 5, vertical_borders, None)
border = Border(width - 5, 5, width - 5, height - 5, vertical_borders, None)

for i in range(800):
    Pulya(all_enemies, i, random.randint(0, 600))

if gaming:

    while running:

        all_sprites.draw(screen)
        Pulya(all_enemies, 800, random.randint(0, 600))
        spawn(point)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Bullet(all_bullets, hero1.rect.x, hero1.rect.y)

            hero1.event(event)

        screen.fill((0, 0, 0))
        draw(point)
        draw2(lifes)

        all_enemies.update()
        points(point)
        all_bullets.update()
        all_hostiles.update()
        lose(losing_border, all_hostiles)
        out_of_range(border, all_bullets)
        kill(all_hostiles, all_bullets)
        all_bullets.draw(screen)

        all_enemies.draw(screen)
        all_sprites.draw(screen)
        all_hostiles.draw(screen)

        clock.tick(50)

        pygame.display.flip()

        print(lifes)
        if lifes <= 0:
            gaming = False
            break

if not gaming:
    gameoverScreen(point)

pygame.quit()
