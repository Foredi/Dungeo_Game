import pygame
import math
from sys import exit
import os
import numpy as np
from setting import *
from spritesheet import *
from animation import *
from player import *
from camera import *
from enemy import *
from algorithm import *

pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Dungeon")
clock = pygame.time.Clock()

grid = np.genfromtxt("img/maps/map1.csv", delimiter=",", dtype=int)

player = Player(PLAYER_SPEED, LoadAnimation("img/character").load_animation())

camera = Camera(pygame.image.load("img/maps/map1.png").convert_alpha(), grid)

all_sprites_group = pygame.sprite.Group()
enemy = pygame.sprite.Group()

slime1 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime2 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime3 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime4 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime5 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime6 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime7 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime8 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime9 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime10 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime11 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime12 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime13 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime14 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime15 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime16 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime17 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime18 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime19 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime20 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime21 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime22 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime23 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
slime24 = Slime(LoadAnimation("img/enemy/Slime").load_animation(), enemy, all_sprites_group, grid)
all_sprites_group.add(player)

win = pygame.transform.rotozoom(pygame.image.load("img/win.jpg").convert_alpha(), 0, 2.5)
lost = pygame.transform.rotozoom(pygame.image.load("img/over.jpg").convert_alpha(), 0, 1)

while True:
    keys = pygame.key.get_pressed()
    # Set the FPS
    clock.tick(FPS)

    # Update the screen
    screen.fill(BLACK)

    camera.custom_draw(player, enemy)

    if grid[np.round(player.pos.y // TILESIZE).astype(int) + 1][np.round(player.pos.x // TILESIZE).astype(int) + 1] == 183 or grid[np.round(player.pos.y // TILESIZE).astype(int) + 1][np.round(player.pos.x // TILESIZE).astype(int) + 1] == 184:
        screen.blit(win, (0, 0))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        exit()
    
    if player.health <= 0:
        screen.blit(lost, (0, 0))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        exit()

    # Get all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    pygame.display.update()