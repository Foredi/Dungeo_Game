import pygame
import math
from sys import exit
import os
from setting import *
from spritesheet import *
from animation import *
from player import *

pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon")
clock = pygame.time.Clock()

# Load images character
images = {}

def import_img(path):
    return [pygame.image.load(path + "/" + file).convert_alpha() for file in os.listdir(path)]

for folder in os.listdir("img/character"):
    images[folder] = import_img("img/character/" + folder)


#Create animation list
animation = {}
action = "idle"
move = "front"
moves = {"back": 0, "front": 1, "left": 2, "right": 3}
last_update = pygame.time.get_ticks()
animation_cooldown = 250
frame = 0
is_moving = False
is_attacker = False

player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, LoadAnimation("img/character").load_animation())

# Load animation
for key, value in images.items():
    animation[key] = load_animation(value, [])

while True:
    keys = pygame.key.get_pressed()
    # Set the FPS
    clock.tick(FPS)

    # Update the screen
    screen.fill((0, 0, 0))
    
    current_time = pygame.time.get_ticks()
    if current_time - last_update > animation_cooldown:
        last_update = current_time
        frame += 1
        if frame >= len(animation[action][moves[move]]):
            frame = 0
            if action == "run" and not is_moving:
                action = "idle"
            elif action == "attack":
                action = "idle"
                is_attacker = False

    screen.blit(animation[action][moves[move]][frame], (PLAYER_START_X, PLAYER_START_Y))

    player.update()
    player.draw(screen)
    player.move_player(keys)

    # Get all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # Move the player
            if event.key == pygame.K_a:
                move = "left"
                action = "run"
                is_moving = True
            elif event.key == pygame.K_d:
                move = "right"
                action = "run"
                is_moving = True
            elif event.key == pygame.K_w:
                move = "back"
                action = "run"
                is_moving = True
            elif event.key == pygame.K_s:
                move = "front"
                action = "run"
                is_moving = True
            elif event.key == pygame.K_SPACE:
                if not is_attacker:
                    is_attacker = True
                    action = "attack"
                    frame = 0
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                is_moving = False
        

    if keys[pygame.K_a]:
        PLAYER_START_X -= PLAYER_SPEED
    elif keys[pygame.K_d]:
        PLAYER_START_X += PLAYER_SPEED
    elif keys[pygame.K_w]:
        PLAYER_START_Y -= PLAYER_SPEED
    elif keys[pygame.K_s]:
        PLAYER_START_Y += PLAYER_SPEED


    pygame.display.update()