import pygame
from pygame.locals import *
import random

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800, 550))
pygame.display.set_caption('Flappy Bird')

game_over = False
exit_game = False
scroll = 0
scroll_speed = 5
flying = False
game_over = False
pipe_gap = 300
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
restart_img = pygame.image.load("restart.png")
restart_img = pygame.transform.scale(restart_img, (200, 80))
start_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(start_img, (200, 80))
bg = pygame.image.load('bg.png')
bg = pygame.transform.scale(bg, (800, 600))
G_bg = pygame.image.load("G_BG.png")
G_bg = pygame.transform.scale(G_bg, (900, 250))

clock = pygame.time.Clock()
fps = 40

class bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    def update(self):
        if flying or game_over:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < 450:
                self.rect.y += int(self.vel)
                self.counter += 1
  
            if flying:
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -8
                    pygame.mixer.music.load("Flappy_wing.mp3")
                    pygame.mixer.music.play()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            if self.counter > 10:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            if game_over:
                self.image = pygame.transform.rotate(self.images[self.index], -90)



            else:
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], 0)
        if self.rect.bottom >= 450:
            self.rect.bottom = 450
            self.vel = 0
class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y + int(pipe_gap/2)]
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

flappy = bird(400, int(550/2))
bird_group = pygame.sprite.Group()
bird_group.add(flappy)
pipe_group = pygame.sprite.Group()

def reset_game():
    pipe_group.empty()
    flappy.rect.center = (400, int(550/2))
    flappy.vel = 0
    return False

while not exit_game:
    clock.tick(fps)

    screen.blit(bg, (0, 0))
    screen.blit(G_bg, (scroll, 450))
    if not game_over:
        scroll -= scroll_speed

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    if abs(scroll) > 50:
        scroll = 0
    if not game_over:
        pipe_group.update()

    if game_over:
        button_rect = restart_img.get_rect(center=(400, 350))
        screen.blit(restart_img, button_rect)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        if not game_over:
            pygame.mixer.music.load("Flappy_die.mp3")
            pygame.mixer.music.play()
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        pipe_height = random.randint(-100,100)
        if time_now - last_pipe > pipe_frequency:
            btm_pipe = pipe(800, 300 + pipe_height,-1)
            top_pipe = pipe(800, 300 + pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

    start_rect = start_img.get_rect(center=(400, 350))
    if not flying and not game_over:
        screen.blit(start_img, start_rect)
                    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not flying and not game_over:
                if start_rect.collidepoint(event.pos):
                    flying = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if button_rect.collidepoint(event.pos):
                    game_over = False
                    flying = reset_game()
    pygame.display.update()

pygame.quit()
quit()