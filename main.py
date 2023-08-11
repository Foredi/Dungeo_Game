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

player_sprite = pygame.sprite.Group()
player_sprite.add(player)

class Camera():
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        self.ground = pygame.transform.rotozoom(pygame.image.load("img/maps/map1.png").convert_alpha(), 0, 2.5)
        self.ground_rect = self.ground.get_rect(topleft = (0, 0))

    def center_target_camera(self, target):
        # Tính toán vị trí mới cho camera
        new_offset = pygame.math.Vector2(
            self.half_w - target.rect.centerx,
            self.half_h - target.rect.centery
        )

        # Kiểm tra nếu vị trí mới vượt quá biên của ground thì không cập nhật offset
        if self.ground_rect.left + new_offset.x > 0:
            new_offset.x = -self.ground_rect.left
        elif self.ground_rect.right + new_offset.x < WIDTH:
            new_offset.x = WIDTH - self.ground_rect.right

        if self.ground_rect.top + new_offset.y > 0:
            new_offset.y = -self.ground_rect.top
        elif self.ground_rect.bottom + new_offset.y < HEIGHT:
            new_offset.y = HEIGHT - self.ground_rect.bottom

        self.offset = new_offset


    def custom_draw(self):
        self.center_target_camera(player)
        ground_rect = self.ground_rect.topleft + self.offset
        self.display_surface.blit(self.ground, ground_rect)

        for sprite in sorted(player_sprite, key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            sprite.update()
            self.display_surface.blit(sprite.image, offset_pos)

camera = Camera()


while True:
    keys = pygame.key.get_pressed()
    # Set the FPS
    clock.tick(FPS)

    # Update the screen
    screen.fill(BLACK)

    camera.custom_draw()

    # Get all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    pygame.display.update()