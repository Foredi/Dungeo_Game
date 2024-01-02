from spritesheet import *
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
                    temp_list.append(sprite_sheet.get_image(i, height, height, 2.5, BLACK))
                temp_animation.append(temp_list)
            self.animation[key] = temp_animation
        return self.animation