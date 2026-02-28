import pygame
import random
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake")

pygame.display.update()

clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 55)
def text_screen(text,colour,x,y):
    screen_text = font.render(text, True, colour)
    screen.blit(screen_text, [x,y])

def plot_snake(screen, colour, snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(screen,(255,255,255),[x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        screen.fill((255, 255, 255))
        text_screen("Welcome to Snakes", (0, 0, 0), 200, 200)
        text_screen("Press Space Bar to play", (0, 0, 0), 200, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('snakecharmer.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)
def gameloop():
    exit_game = False
    game_over = False

    snk_list = []
    snk_length = 1

    score = 0

    with open("highscore.txt","r") as f:
        highscore = f.read()

    snake_x = 100
    snake_y = 100
    snake_size = 10
    velocity_x = 0
    velocity_y = 0


    food_x = random.randint(0, 800)
    food_y = random.randint(0,600)

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            screen.fill((255,255,255))
            text_screen("Game Over! Press Enter To Continue", (0, 0, 0), 80, 100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                            exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - 5
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - 5
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = 5
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                food_x = random.randint(0, 800)
                food_y = random.randint(0, 600)
                pygame.mixer.music.load('nom_nom_nom.mp3')
                pygame.mixer.music.play()
                score += 1
                snk_length +=5
                if score > int(highscore):
                    highscore = score

            screen.fill((0, 0, 0))

            text_screen("Score: " + str(score) + "  Hiscore: " + str(highscore), (255, 255, 255), 2, 2)

            pygame.draw.rect(screen, (255, 0, 0), [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
            
            if snake_x<0 or snake_x>800 or snake_y<0 or snake_y>600:
                game_over = True

            plot_snake(screen, (255, 255, 255), snk_list, snake_size)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
welcome()