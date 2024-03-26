import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
background_img = pygame.image.load('img/space4.jpg')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Игра Комета")
icon = pygame.image.load("img/tir2.jpg")
pygame.display.set_icon(icon)

target_img = pygame.image.load("img/kometa2.png")
target_width = 80
target_height = 80

star_img = pygame.image.load("img/star.png")
star_width = 20
star_height = 20

target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

stars = []
score = 0
font = pygame.font.Font(None, 36)

hit_sound = pygame.mixer.Sound('hit_sound.wav')
hit_sound.set_volume(0.2)

target_speed = 0.5
target_angle = random.randint(0, 360)

target_img.set_alpha(180)  # Прозрачность мишени (от 0 до 255)
screen.blit(target_img, (target_x, target_y))

def update_target_position():
    global target_x, target_y, target_angle
    target_x += target_speed * math.cos(target_angle)
    target_y += target_speed * math.sin(target_angle)

    if target_x <= 0 or target_x + target_width >= SCREEN_WIDTH or target_y <= 0 or target_y + target_height >= SCREEN_HEIGHT:
        target_angle = random.randint(0, 360)

def explode_stars(x, y):
    for _ in range(10):
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 1])
        star_x = x + random.randint(0, target_width) * direction_x
        star_y = y + random.randint(0, target_height) * direction_y
        stars.append((star_x, star_y))

def calculate_score():
    global score
    score += 1

running = True
clock = pygame.time.Clock()
while running:
    screen.blit(background_img, (0, 0))
    # screen.fill(color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                explode_stars(target_x, target_y)
                hit_sound.play()
                calculate_score()
                target_speed += 0.3  # Увеличиваем скорость движения мишени
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)

    update_target_position()

    for star in stars:
        screen.blit(star_img, star)

    stars = [(x, y + 0.2) for x, y in stars]
    stars = [(x, y) for x, y in stars if y < SCREEN_HEIGHT]

    screen.blit(target_img, (target_x, target_y))
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    screen.blit(score_text,(10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
