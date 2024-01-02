import pygame
from spritesheet import SpriteSheet
from setting import *
from animation import *
from algorithm import *
import os
import math
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self , speed, animation):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = speed
        self.animation = animation
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animation_cooldown = 250
        self.velocity_x = 0
        self.velocity_y = 0
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
        self.rect.height = self.hitbox_rect.height - 35
        self.rect.width = self.hitbox_rect.width - 35

    def user_input(self, grid):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            next_grid = np.round((self.pos + pygame.math.Vector2(5 * -self.speed, 0)) // TILESIZE).astype(int) + 1
            if grid[next_grid[1]][next_grid[0]] == 27 or grid[next_grid[1]][next_grid[0]] == 183 or grid[next_grid[1]][next_grid[0]] == 184:
                self.velocity_x = -self.speed
            else:
                self.velocity_x = 0
            # self.velocity_x = -self.speed
            # self.action = "run"
            self.move = "left"
            # self.is_moving = True
        if keys[pygame.K_d]:
            next_grid = np.round((self.pos + pygame.math.Vector2(5 * self.speed, 0)) // TILESIZE).astype(int) + 1
            if grid[next_grid[1]][next_grid[0]] == 27 or grid[next_grid[1]][next_grid[0]] == 183 or grid[next_grid[1]][next_grid[0]] == 184:
                self.velocity_x = self.speed
            else:
                self.velocity_x = 0
            # self.velocity_x = self.speed
            # self.action = "run"
            self.move = "right"
            # self.is_moving = True
        if keys[pygame.K_w]:
            next_grid = np.round((self.pos + pygame.math.Vector2(0, 5 * -self.speed)) // TILESIZE).astype(int) + 1
            if grid[next_grid[1]][next_grid[0]] == 27 or grid[next_grid[1]][next_grid[0]] == 183 or grid[next_grid[1]][next_grid[0]] == 184: 
                self.velocity_y = -self.speed
            else:
                self.velocity_y = 0
            # self.velocity_y = -self.speed
            # self.action = "run"
            self.move = "back"
            # self.is_moving = True
        if keys[pygame.K_s]:
            next_grid = np.round((self.pos + pygame.math.Vector2(0, 10 * self.speed)) // TILESIZE).astype(int) + 1
            if grid[next_grid[1]][next_grid[0]] == 27 or grid[next_grid[1]][next_grid[0]] == 183 or grid[next_grid[1]][next_grid[0]] == 184:
                self.velocity_y = self.speed
            else:
                self.velocity_y = 0
            # self.velocity_y = self.speed
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

    def auto_move(self, grid):
        grid_row = np.round(self.pos.y // TILESIZE).astype(int) + 1
        grid_col = np.round(self.pos.x // TILESIZE).astype(int) + 1
        grid_row_chest = np.round(1300 // TILESIZE).astype(int) + 1
        grid_col_chest = np.round(2300 // TILESIZE).astype(int) + 1
        a = Algorithm(grid.shape[0], grid.shape[1], grid)
        path = a.getPath((grid_row, grid_col), (grid_row_chest, grid_col_chest), "BFS")
        if path:
            next_grid = path.pop(0)
            next_pos = pygame.math.Vector2(next_grid[1] * TILESIZE, next_grid[0] * TILESIZE)
            if next_pos != self.pos:
                self.direction = (next_pos - self.pos).normalize()
            else:
                self.direction = pygame.math.Vector2(5, 5)
            self.velocity = self.direction * self.speed
            self.pos += self.velocity
            self.rect.centerx = self.pos.x
            self.rect.centery = self.pos.y


    def update(self, grid):
        self.user_input(grid)
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





    

