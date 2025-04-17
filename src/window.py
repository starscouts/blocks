import sys

import pygame

def init():
    pygame.display.set_caption("Blocks")

    if sys.platform == "darwin":
        pygame.display.set_icon(pygame.image.load('./assets/textures/icon-mac.png').convert_alpha())
    else:
        pygame.display.set_icon(pygame.image.load('./assets/textures/icon.png').convert_alpha())

    pygame.mouse.set_visible(True)
