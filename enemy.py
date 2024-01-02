import pygame
import numpy as np
from setting import *
from animation import *
from algorithm import *

class Slime(pygame.sprite.Sprite):
    def __init__(self, animation, enemy_group, all_sprites_group, grid):
        super().__init__(enemy_group, all_sprites_group)
        self.pos = self.generate_valid_position(grid)
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        self.animation = animation
        self.animation_steps = 4
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250
        self.frame = 0
        self.action = "idle"
        self.view = "front"
        self.moves = {"front": 0, "side": 1}

        self.image = self.animation[self.action][self.moves[self.view]][self.frame]
        self.rect = self.image.get_rect(center = (WIDTH // 2, HEIGHT // 2))

        self.speed = ENEMY_SPEED
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(0, 0)

    def generate_valid_position(self, grid):
        while True:
            x = np.random.randint(0, grid.shape[1])
            y = np.random.randint(0, grid.shape[0])
            if grid[y][x] == 27:
                return pygame.math.Vector2(x * TILESIZE, y * TILESIZE)

    def hunt_player(self, player, grid):
        grid_row = np.round(self.pos.y // TILESIZE).astype(int) + 1
        grid_col = np.round(self.pos.x // TILESIZE).astype(int) + 1
        grid_row_player = np.round(player.pos.y // TILESIZE).astype(int) + 1
        grid_col_player = np.round(player.pos.x // TILESIZE).astype(int) + 1
        a = Algorithm(grid.shape[0], grid.shape[1], grid)
        path = a.getPath((grid_row, grid_col), (grid_row_player, grid_col_player), "BFS")

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
            
            # Khi đến gần người chơi, slime sẽ chuyển từ trạng thái "idle" sang trạng thái "attack"
            if self.rect.colliderect(player.rect):
                self.action = "attack"
                self.view = "side"
                self.image = self.animation[self.action][self.moves[self.view]][self.frame]
                player.health -= 1
            else:
                self.action = "idle"
                self.view = "front"
                self.image = self.animation[self.action][self.moves[self.view]][self.frame]

            if self.rect.colliderect(player.rect):
                self.kill()

        time_game = a.getTimeAll((grid_row, grid_col), (grid_row_player, grid_col_player), 20)
        # pygame.display.set_caption("Shadow Dungeon - " + time_game[0] + " - " + str(time_game[1]))
        pygame.display.set_caption("Shadow Dungeon - " + str(time_game[0]) + " - " + str(time_game[1]))


    def get_vector_distance(self, vector1, vector2):
        return (vector1 - vector2).magnitude()

    def update(self, player, grid):
        player_distance = self.get_vector_distance(player.pos, self.pos)
        if player_distance <= 7 * TILESIZE:
            self.hunt_player(player, grid)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_cooldown:
            self.last_update = current_time
            self.frame += 1
            if self.frame >= len(self.animation[self.action][self.moves[self.view]]):
                self.frame = 0
            self.image = self.animation[self.action][self.moves[self.view]][self.frame]
