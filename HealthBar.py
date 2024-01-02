import pygame
from setting import *
from spritesheet import *

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.Surface((player.rect.width, 10))  # Chiều rộng và chiều cao của thanh health bar
        self.image.fill((255, 0, 0)) # Màu sắc của thanh health bar
        self.rect = self.image.get_rect() # Lấy hình chữ nhật bao quanh thanh health bar
        self.rect.midbottom = self.player.rect.midtop

    def update(self):
        # Cập nhật lại màu sắc cho lượng máu đã mất của thanh health bar
        self.image = pygame.Surface((self.player.rect.width, 10))
        self.image.fill((255, 0, 0))
        # Tính chiều rộng của phần máu còn lại
        ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, self.player.rect.width * ratio, 10))


# người chơi có 3 trái tim (3 mạng) hiển thị trên goóc trên bên trái màn hình game
class Heart(pygame.sprite.Sprite):
    def __init__(self, hearth_full, hearth_half, hearth_empty):
        super().__init__()
        self.hearth_full = hearth_full
        self.hearth_half = hearth_half
        self.hearth_empty = hearth_empty
        self.image = self.hearth_full
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def update(self, player):
        # Tính toán lại số lượng trái tim cần hiển thị
        if player.health % 3 == 0:
            self.image = self.hearth_full
        elif player.health % 3 == 2:
            self.image = self.hearth_half
        elif player.health % 3 == 1:
            self.image = self.hearth_empty
        else:
            self.image = self.hearth_empty
        # Hiển thị trái tim lên màn hình
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

class HeartManager(pygame.sprite.Group):
    def __init__(self, all_sprites_group, num_heart, heart_full, heart_half, heart_empty):
        super().__init__(all_sprites_group)
        self.num_heart = num_heart
        self.heart = []

        for i in range(self.num_heart):
            heart = Heart(heart_full, heart_half, heart_empty)
            heart.rect = (heart.rect.x + i * 32, heart.rect.y)
            self.add(heart)
            self.heart.append(heart)

    def update(self, player):
        i = self.num_heart - 1
        if player.health <= 6:
            self.heart[2].kill()
            i = 1
        if player.health <= 3:
            self.heart[1].kill()
            i = 0
        if player.health < 1:
            self.heart[0].kill()

        self.heart[i].update(player)
        self.heart[i].rect = (self.heart[i].rect.x + i * 32, self.heart[i].rect.y)

            


