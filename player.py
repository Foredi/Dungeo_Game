import pygame
from spritesheet import SpriteSheet
from setting import *
import os

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
                    temp_list.append(sprite_sheet.get_image(i, 32, 32, 3, BLACK))
                temp_animation.append(temp_list)
            self.animation[key] = temp_animation
        return self.animation

class Player():
    def __init__(self, x, y, speed, animation):
        self.x = x
        self.y = y
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

    def update(self):
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


    def draw(self, screen):
        screen.blit(self.animation[self.action][self.moves[self.move]][self.frame], (self.x, self.y))

    def move_player(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.move = "back"
            self.action = "run"
            self.is_moving = True
        elif keys[pygame.K_s]:
            self.y += self.speed
            self.move = "front"
            self.action = "run"
            self.is_moving = True
        elif keys[pygame.K_a]:
            self.x -= self.speed
            self.move = "left"
            self.action = "run"
            self.is_moving = True
        elif keys[pygame.K_d]:
            self.x += self.speed
            self.move = "right"
            self.action = "run"
            self.is_moving = True
        else:
            self.is_moving = False

    def attack(self, keys):
        if keys[pygame.K_SPACE]:
            self.action = "attack"
            self.is_attacker = True
