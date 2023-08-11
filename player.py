import pygame
from spritesheet import SpriteSheet
from setting import *
import os
import math

class LoadAnimation():
    def __init__(self, path):
        self.path = path
        self.images = {folder: [pygame.image.load(self.path + "/" + folder + "/" + file).convert_alpha() for file in os.listdir(self.path + "/" + folder)] for folder in os.listdir(self.path)}
        self.animation = {}
    
    def load_animation(self):
        for key, values in self.images.items():
            temp_animation = []
            for value in values:
                sprite_sheet = SpriteSheet(value)
                temp_list = []
                wigth, height = value.get_size()
                for i in range(wigth // height):
                    temp_list.append(sprite_sheet.get_image(i, 32, 32, 2.5, BLACK))
                temp_animation.append(temp_list)
            self.animation[key] = temp_animation
        return self.animation

class Player(pygame.sprite.Sprite):
    def __init__(self , speed, animation):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = speed
        self.animation = animation
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animation_cooldown = 250
        self.action = "idle"
        self.move = "front"
        self.moves = {"back": 0, "front": 1, "left": 2, "right": 3}
        self.is_moving = False
        self.is_attacker = False
        self.base_player_image = self.animation[self.action][self.moves[self.move]][self.frame]
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos + pygame.math.Vector2(48, 48))
        self.rect = self.hitbox_rect.copy()
        self.image = self.base_player_image

    def player_rotate(self):
        self.base_player_image = self.animation[self.action][self.moves[self.move]][self.frame]
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos + pygame.math.Vector2(48, 48))
        self.rect = self.hitbox_rect.copy()
        self.rect.center = self.hitbox_rect.center + pygame.math.Vector2(10, 10)
        self.rect.height = self.hitbox_rect.height - 20
        self.rect.width = self.hitbox_rect.width - 20

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
            # self.action = "run"
            self.move = "left"
            # self.is_moving = True
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
            # self.action = "run"
            self.move = "right"
            # self.is_moving = True
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
            # self.action = "run"
            self.move = "back"
            # self.is_moving = True
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
            # self.action = "run"
            self.move = "front"
            # self.is_moving = True
        if keys[pygame.K_SPACE]:
            if not self.is_attacker:
                self.is_attacker = True
                self.action = "attack"
                self.frame = 0

        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.is_moving = True
            self.action = "run"
            # self.frame = 0
            self.is_attacker = False
        
        if self.velocity_x == 0 and self.velocity_y == 0:
            self.is_moving = False

    def move_camera(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def update(self):
        self.user_input()
        self.move_camera()
        self.player_rotate()
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_cooldown:
            self.last_update = current_time
            self.frame += 1
            if self.frame >= len(self.animation[self.action][self.moves[self.move]]):
                self.frame = 0
                if self.action == "run" and not self.is_moving:
                    self.action = "idle"
                elif self.action == "attack":
                    self.action = "idle"
                    self.is_attacker = False
        self.image = self.animation[self.action][self.moves[self.move]][self.frame]

    def draw(self, screen, pos = None):
        self.update()
        if pos:
            screen.blit(self.animation[self.action][self.moves[self.move]][self.frame], pos)
        else:
            screen.blit(self.animation[self.action][self.moves[self.move]][self.frame], self.pos)





    

