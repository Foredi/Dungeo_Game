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

player = Player(PLAYER_SPEED, LoadAnimation("img/character").load_animation())

while True:
    keys = pygame.key.get_pressed()
    # Set the FPS
    clock.tick(FPS)

    # Update the screen
    screen.fill((255, 255, 255))

    player.draw(screen)

    # Get all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    pygame.display.update()