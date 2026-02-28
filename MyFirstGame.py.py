import pygame
import sys
import random
import time


pygame.init()

player_max_hp = 100
player_hp = 100
player_regen_rate = 2  # HP per second
last_regen_time = pygame.time.get_ticks()

game_over = False

# Bullet Settings
bullets = []
bullet_width = 4
bullet_length = 15   # 🔥 CHANGE THIS to increase laser length
bullet_speed = 25
bullet_fire_rate = 10  # bullets per second (CHANGE THIS anytime)
bullet_delay = 1000 / bullet_fire_rate  # milliseconds
last_shot_time = 0

# Get user screen size
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Create fullscreen window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("WASD Square Game")

# Square settings
square_size = 40
x = WIDTH // 2 - square_size // 2
y = HEIGHT // 2 - square_size // 2
speed = 7

clock = pygame.time.Clock()


enemy_size = 40
enemies = []

spawn_delay = 1300  # 2000 milliseconds = 2 seconds
last_spawn_time = pygame.time.get_ticks()

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    
    if side == "top":
        x = random.randint(0, WIDTH)
        y = -enemy_size  # spawn outside screen
        vx = 0
        vy = random.randint(5, 7)

    elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT + enemy_size
        vx = 0
        vy = -random.randint(5, 7)

    elif side == "left":
        x = -enemy_size
        y = random.randint(0, HEIGHT)
        vx = random.randint(5, 7)
        vy = 0

    else:  # right
        x = WIDTH + enemy_size
        y = random.randint(0, HEIGHT)
        vx = -random.randint(5, 7)
        vy = 0

    hp = random.randint(80, 100)
    enemies.append([x, y, vx, vy, hp])

running = True
while running:
    clock.tick(60)  # 60 FPS

    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # 🔥 Restart Game
            if game_over and event.key == pygame.K_r:
                # Reset all variables
                player_hp = 100
                x = WIDTH // 2 - square_size // 2
                y = HEIGHT // 2 - square_size // 2
                enemies.clear()
                bullets.clear()
                game_over = False

    
    if not game_over:
        # Shooting Logic (Hold Left Click)
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0]:  # Left mouse button
            if current_time - last_shot_time >= bullet_delay:
                mx, my = pygame.mouse.get_pos()

                # Calculate direction
                dx = mx - (x + square_size // 2)
                dy = my - (y + square_size // 2)

                length = (dx ** 2 + dy ** 2) ** 0.5
                if length != 0:
                    dx /= length
                    dy /= length

                # Bullet velocity
                vx = dx * bullet_speed
                vy = dy * bullet_speed

                # Spawn bullet from player center
                bullets.append([
                    x + square_size // 2,
                    y + square_size // 2,
                    vx,
                    vy,
                    dx,   # direction x (normalized)
                    dy    # direction y
                ])

                last_shot_time = current_time

        # Player HP Regen
        if current_time - last_regen_time >= 1000:  # 1000ms = 1 second
            if player_hp < player_max_hp:
                player_hp += player_regen_rate
                if player_hp > player_max_hp:
                    player_hp = player_max_hp
            last_regen_time = current_time

        if current_time - last_spawn_time > spawn_delay:
            spawn_enemy()
            last_spawn_time = current_time

        # Move Enemies Toward Player
        for enemy in enemies:
            dx = x - enemy[0]
            dy = y - enemy[1]

            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance != 0:
                dx /= distance
                dy /= distance

            enemy_speed = 2  # 🔥 change speed here
            enemy[0] += dx * enemy_speed
            enemy[1] += dy * enemy_speed

        # Move Bullets
        for bullet in bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]

            if (bullet[0] < 0 or bullet[0] > WIDTH or
                bullet[1] < 0 or bullet[1] > HEIGHT):
                bullets.remove(bullet)
        
        
        # Bullet Collision With Enemies
        for bullet in bullets[:]:

            bullet_rect = pygame.Rect(
                bullet[0] - bullet_width // 2,
                bullet[1] - bullet_width // 2,
                bullet_width,
                bullet_width
            )

            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(
                    enemy[0],
                    enemy[1],
                    enemy_size,
                    enemy_size
                )

                if bullet_rect.colliderect(enemy_rect):
                    enemy[4] -= 20
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break
        
        player_rect = pygame.Rect(x, y, square_size, square_size)

        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)

            if player_rect.colliderect(enemy_rect):
                player_hp -= 1  # player takes damage

        if player_hp <= 0:
            player_hp = 0
            game_over = True

        import math

        def normalize_movement(dx, dy, speed):
            length = math.sqrt(dx * dx + dy * dy)
            
            if length != 0:
                dx = dx / length
                dy = dy / length
            
            return dx * speed, dy * speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Press ESC to exit fullscreen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get pressed keys
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        # Normalize movement
        dx, dy = normalize_movement(dx, dy, speed)

        x += dx
        y += dy

        # Prevent going outside screen
        x = max(0, min(WIDTH - square_size, x))
        y = max(0, min(HEIGHT - square_size, y))

        # Draw background
        screen.fill((25, 25, 40))

        # Draw player
        pygame.draw.rect(screen, (0, 255, 100), (x, y, square_size, square_size))

        # Health Bar Settings
        bar_width = square_size
        bar_height = 6
        gap = 8  # little gap above player

        health_ratio = player_hp / player_max_hp
        current_bar_width = bar_width * health_ratio

        # Red Background
        pygame.draw.rect(screen, (150, 0, 0),
                        (x, y - gap - bar_height, bar_width, bar_height))

        # Green Current HP
        pygame.draw.rect(screen, (0, 255, 0),
                        (x, y - gap - bar_height, current_bar_width, bar_height))
        
        #Ememy draw
        for enemy in enemies[:]:
            if enemy[4] <= 0:
                enemies.remove(enemy)
            else:
                # Draw enemy
                pygame.draw.rect(screen, (255, 0, 0),
                                (enemy[0], enemy[1], enemy_size, enemy_size))

                # Enemy Health Bar
                enemy_max_hp = 100
                bar_width = enemy_size
                bar_height = 5
                gap = 6

                health_ratio = enemy[4] / enemy_max_hp
                current_bar_width = bar_width * health_ratio

                # Red background
                pygame.draw.rect(screen, (120, 0, 0),
                                (enemy[0],
                                enemy[1] - gap - bar_height,
                                bar_width,
                                bar_height))

                # Green current HP
                pygame.draw.rect(screen, (0, 255, 0),
                                (enemy[0],
                                enemy[1] - gap - bar_height,
                                current_bar_width,
                                bar_height))
                            
        # Draw Laser Bullets
        for bullet in bullets:
            start_x = bullet[0]
            start_y = bullet[1]

            end_x = start_x - bullet[4] * bullet_length
            end_y = start_y - bullet[5] * bullet_length

            pygame.draw.line(
                screen,
                (255, 255, 0),  # Yellow laser
                (start_x, start_y),
                (end_x, end_y),
                bullet_width
            )

        if game_over:
            # Red transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)  # 50% opacity
            overlay.fill((255, 0, 0))
            screen.blit(overlay, (0, 0))

            # Big "YOU DIED" text
            font = pygame.font.SysFont(None, 150)  # big size
            text = font.render("YOU DIED", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(text, text_rect)

            # Small "Press R to Restart" text
            small_font = pygame.font.SysFont(None, 50)  # smaller size
            restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
            screen.blit(restart_text, restart_rect)

        pygame.display.update()

pygame.quit()
sys.exit()