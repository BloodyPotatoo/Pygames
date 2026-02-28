import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprites")

clock = pygame.time.Clock()


# ================= PLAYER CLASS =================
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 250

        # -------- LOAD SPRITES MANUALLY --------
        self.animations = {
            "idle": [
                pygame.transform.scale(pygame.image.load("Z_right.png").convert_alpha(), (130, 130)),
                pygame.transform.scale(pygame.image.load("Z_right.png").convert_alpha(), (130, 130))
            ],
            "up": [
                pygame.transform.scale(pygame.image.load("Z_up.png").convert_alpha(), (130, 130)),
                pygame.transform.scale(pygame.image.load("Z_up.png").convert_alpha(), (130, 130))
            ],
            "down": [
                pygame.transform.scale(pygame.image.load("Z_down.png").convert_alpha(), (130, 130)),
                pygame.transform.scale(pygame.image.load("Z_down.png").convert_alpha(), (130, 130))
            ],
            "left": [
                pygame.transform.scale(pygame.image.load("Z_left.png").convert_alpha(), (130, 130)),
                pygame.transform.scale(pygame.image.load("Z_left.png").convert_alpha(), (130, 130))
            ],
            "right": [
                pygame.transform.scale(pygame.image.load("Z_right.png").convert_alpha(), (130, 130)),
                pygame.transform.scale(pygame.image.load("Z_right.png").convert_alpha(), (130, 130))
            ]
        }

        self.current_animation = self.animations["idle"]
        self.frame_index = 0
        self.animation_speed = 10
        self.image = self.current_animation[self.frame_index]

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy = -1
            self.current_animation = self.animations["up"]

        if keys[pygame.K_s]:
            dy = 1
            self.current_animation = self.animations["down"]

        if keys[pygame.K_a]:
            dx = -1
            self.current_animation = self.animations["left"]

        if keys[pygame.K_d]:
            dx = 1
            self.current_animation = self.animations["right"]

        # Fix diagonal speed
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        if dx == 0 and dy == 0:
            self.current_animation = self.animations["idle"]

        self.rect.center = (self.x, self.y)

    def update_animation(self, dt):
        self.frame_index += self.animation_speed * dt

        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0

        self.image = self.current_animation[int(self.frame_index)]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ================= GAME LOOP =================
player = Player(WIDTH // 2, HEIGHT // 2)

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move(dt)
    player.update_animation(dt)

    screen.fill((0, 0, 0))
    player.draw(screen)

    pygame.display.update()

pygame.quit()