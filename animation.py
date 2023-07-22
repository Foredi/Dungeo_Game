from spritesheet import *
from setting import *

def load_animation(images, animation_list):
    for image in images:
        sprite_sheet = SpriteSheet(image)
        temp_list = []
        wight, height = image.get_size()
        for i in range(wight // height):
            temp_list.append(sprite_sheet.get_image(i, 32, 32, 3, BLACK))
        animation_list.append(temp_list)
    return animation_list