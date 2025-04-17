import pygame
from math import floor

texture_map = pygame.image.load('./assets/textures/intro_atlas.png').convert_alpha()
preloaded = []

for i in range(8):
    for j in range(8):
        preloaded.append(texture_map.subsurface((360 * j, 360 * i, 360, 360)))

def draw_texture(id):
    return preloaded[id]

def unload_intro():
    global texture_map
    del texture_map