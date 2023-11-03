import os

import pygame

from constants import SCALE, WEAPON_SCALE


def scale_img(img,scale):
    w = img.get_width()
    h = img.get_height()
    new_img = pygame.transform.scale(img,(w * scale,h * scale))
    return new_img

def load_animations(character,animation_Map):
    for animation in animation_Map.keys():
        print(animation)
        try:
            for i in range(len(os.listdir(f"assets/images/characters/{character}/{animation}/"))):
                image = pygame.image.load(f"assets/images/characters/{character}/{animation}/{i}.png").convert_alpha()
                image = scale_img(image,SCALE)
                animation_Map[animation].append(image)
        except:
            animation_Map = None
    return animation_Map

def load_weapon_animation(weapon,scale):
    slash_animation = []
    for i in range(len(os.listdir(f"assets/images/weapons/{weapon}/"))):
        image = pygame.image.load(f"assets/images/weapons/{weapon}/{i}.png").convert_alpha()
        image = scale_img(image, scale)
        slash_animation.append(image)
    return slash_animation