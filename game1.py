import pygame
pygame.init()

pygame.display.set_caption('WASD')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player_x = 100
player_y = 100
speed = 5

running = True
while running:
    clock.tick(60)  # 60 FPS smoothness
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_y -= speed
    if keys[pygame.K_s]:
        player_y += speed
    if keys[pygame.K_a]:
        player_x -= speed
    if keys[pygame.K_d]:
        player_x += speed

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, 50, 50))
    pygame.display.update()

pygame.quit()