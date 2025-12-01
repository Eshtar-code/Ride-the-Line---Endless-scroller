import pygame           # doku: pygame.org;   log
from sys import exit
import random

GAME_WIDTH = 640
GAME_HEIGHT = 360

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Ride the Line")
clock = pygame.time.Clock()

ball_x = 25
ball_y = 126

class Ball(pygame.Rect):
    def __init__(self, img):
        ball_width, ball_height = img.get_width(), img.get_height()
        pygame.Rect.__init__(self, ball_x, ball_y, ball_width, ball_height)
        self.img = img

class obstacle(pygame.Rect):
    def __init__(self, img):
        obs_width, obs_height = img.get_width(), img.get_height()
        obstacle_x = GAME_WIDTH
        obstacle_y = random.choice([126, 184])
        pygame.Rect.__init__(self, obstacle_x, obstacle_y, obs_width, obs_height)
        self.img = img
        self.passed = False

background_image = pygame.image.load("Background.png")
ball_image = pygame.image.load("Ball.png")
obstacle_image = pygame.image.load("Obstacle.png")
switch_sfx = pygame.mixer.Sound("position switch sound.wav")
game_over_sfx = pygame.mixer.Sound("game over sound.wav")

ball = Ball(ball_image)
obstacles = []
velocity_x = -3
score = 0
game_over = False

def draw():
    window.blit(background_image, (0, 0))
    window.blit(ball.img, ball)

    for obs in obstacles:
        window.blit(obs.img, obs)

    score_display = str(score)
    if game_over:
        score_display = f"Game over! {score}"

    font = pygame.font.SysFont("Arial", 45)
    text_render = font.render(score_display, True, "White")
    window.blit(text_render, (10, 5))

def get_speed(score):
    if score < 3: return velocity_x
    if score < 6: return velocity_x * 2
    return velocity_x * 3

def move():
    global score, game_over
    speed = get_speed(score)
    for obs in obstacles:
        obs.x += speed


        if not obs.passed and ball.x > obs.x + obs.width:
            score += 1
            obs.passed = True

        if ball.colliderect(obs):
            game_over_sfx.play()
            game_over = True
            return


    while len(obstacles) > 0 and obstacles[0].x < -50:
        obstacles.pop(0)

def create_obstacle():
    obs = obstacle(obstacle_image)
    obstacles.append(obs)

print(len(obstacles))

create_first_obstacle_timer = pygame.USEREVENT + 0
create_obstacles_timer = pygame.USEREVENT + 1
delay = random.randint(1, 250)
pygame.time.set_timer(create_first_obstacle_timer, delay, loops=1)

def set_obstacle_timer():
    if score <= 3:
        delay_two = random.randint(750, 1500)
    elif score <= 6:
        delay_two = random.randint(375, 750)
    else:
        delay_two = random.randint(250, 450)
    pygame.time.set_timer(create_obstacles_timer, delay_two, loops=1)  # + random.random()     # must be randomised later
            # https://stackoverflow.com/questions/31737965/timed-actions-randomized randomise timer intervals

set_obstacle_timer() # starts first obstacle timer

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_first_obstacle_timer and not game_over:
            create_obstacle()
        
        if event.type == create_obstacles_timer and not game_over:
            create_obstacle()
            set_obstacle_timer()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x) and ball.y == 126:
                ball.y = 184
                #pygame.mixer.music.play(loops=1, fade_ms=0)
                switch_sfx.play()
            else:
                ball.y = 126
                #pygame.mixer.music.play(loops=1, fade_ms=0)
                switch_sfx.play()

            if game_over:
                ball.y = 126
                obstacles.clear()
                set_obstacle_timer()
                score = 0
                game_over = False

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)