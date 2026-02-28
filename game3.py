import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiles")

clock = pygame.time.Clock()

# ===== MAP DATA =====
game_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
]

# ===== LOAD IMAGES =====
grass = pygame.image.load("Z_land.png").convert()
grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))

wall = pygame.image.load("Z_land.png").convert()
wall = pygame.transform.scale(wall, (TILE_SIZE, TILE_SIZE))

player_img = pygame.image.load("Z_land.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

player_rect = player_img.get_rect(center=(200, 200))
player_speed = 5

pygame.display.update()

# ===== CREATE WALL RECT LIST =====
wall_rects = []

for row_index, row in enumerate(game_map):
    for col_index, tile in enumerate(row):
        if tile == 1:
            wall_rects.append(
                pygame.Rect(col_index * TILE_SIZE,
                            row_index * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE)
            )

# ===== GAME LOOP =====
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_w]:
        dy = -player_speed
    if keys[pygame.K_s]:
        dy = player_speed
    if keys[pygame.K_a]:
        dx = -player_speed
    if keys[pygame.K_d]:
        dx = player_speed

    # Move X and check collision
    player_rect.x += dx
    for wall_rect in wall_rects:
        if player_rect.colliderect(wall_rect):
            if dx > 0:
                player_rect.right = wall_rect.left
            if dx < 0:
                player_rect.left = wall_rect.right
    
    # Move Y and check collision
    player_rect.y += dy
    for wall_rect in wall_rects:
        if player_rect.colliderect(wall_rect):
            if dy > 0:
                player_rect.bottom = wall_rect.top
            if dy < 0:
                player_rect.top = wall_rect.bottom

    # ===== DRAW =====
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == 0:
                screen.blit(grass, (x, y))
            elif tile == 1:
                screen.blit(wall, (x, y))

    screen.blit(player_img, player_rect)
    pygame.display.flip()


pygame.quit()