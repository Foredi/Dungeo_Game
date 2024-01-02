import pygame
import numpy as np
from setting import *
from algorithm import *
from Point import *
from HealthBar import *

class Camera(pygame.sprite.Group):
    def __init__(self, img_map, grid):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        self.ground = pygame.transform.rotozoom(img_map, 0, 2.5)
        self.ground_rect = self.ground.get_rect(topleft = (0, 0))

        self.grid = grid

    def center_target_camera(self, target):
        new_offset = pygame.math.Vector2(
            self.half_w - target.rect.centerx,
            self.half_h - target.rect.centery
        )

        if self.ground_rect.left + new_offset.x > 0:
            new_offset.x = -self.ground_rect.left
        elif self.ground_rect.right + new_offset.x < WIDTH:
            new_offset.x = WIDTH - self.ground_rect.right

        if self.ground_rect.top + new_offset.y > 0:
            new_offset.y = -self.ground_rect.top
        elif self.ground_rect.bottom + new_offset.y < HEIGHT:
            new_offset.y = HEIGHT - self.ground_rect.bottom

        self.offset = new_offset
        
        
    def custom_draw(self, player, enemy):
        self.center_target_camera(player)
        ground_rect = self.ground_rect.topleft + self.offset
        self.display_surface.blit(self.ground, ground_rect)

        offset_pos_player = player.pos + self.offset
        player.update(self.grid)
        grid_row_player = np.round(player.pos.y // TILESIZE).astype(int) + 1
        grid_col_player = np.round(player.pos.x // TILESIZE).astype(int) + 1
        self.display_surface.blit(player.image, offset_pos_player)

        # Tạo và cập nhật thanh health bar cho người chơi
        # health_bar = HealthBar(player)
        # health_bar.update()
        # health_bar.rect.midbottom = (player.rect.midtop[0] + self.offset.x, player.rect.midtop[1] + self.offset.y)
        # self.display_surface.blit(health_bar.image, health_bar.rect)

        # heart
        heart_full = SpriteSheet(pygame.image.load("img/ui_heart_full.png").convert_alpha()).get_image(0, 32, 32, 2.5, BLACK)
        heart_half = SpriteSheet(pygame.image.load("img/ui_heart_half.png").convert_alpha()).get_image(0, 32, 32, 2.5, BLACK)
        heart_empty = SpriteSheet(pygame.image.load("img/ui_heart_empty.png").convert_alpha()).get_image(0, 32, 32, 2.5, BLACK)
        heart_manager = HeartManager(self, 3, heart_full, heart_half, heart_empty)
        heart_manager.update(player)
        for heart in heart_manager:
            self.display_surface.blit(heart.image, heart.rect)

        for e in enemy:
            offset_pos_emeny = e.pos + self.offset
            e.update(player, self.grid)
            grid_row = np.round(e.pos.y // TILESIZE).astype(int) + 1
            grid_col = np.round(e.pos.x // TILESIZE).astype(int) + 1
            self.display_surface.blit(e.image, offset_pos_emeny)
        # a = Algorithm(self.grid.shape[0], self.grid.shape[1], self.grid)
        # path = a.getPath((grid_row, grid_col), (grid_row_player, grid_col_player), "BFS")
        # for p in path:
        #     offset_pos = pygame.math.Vector2(p[1] * TILESIZE, p[0] * TILESIZE) + self.offset
        #     pygame.draw.circle(self.display_surface, (255, 0, 0), offset_pos, 5)
        
        