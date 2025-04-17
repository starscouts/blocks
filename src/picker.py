import pygame

import helper
from blocks import blocks
import audio

def show(mouse):
    surface = pygame.Surface((1280, 720))
    surface.fill((0, 0, 0, 128))

    surface.blit(helper.text("Select a block:", 20, (255, 255, 255)), (50, 50))

    x = 50
    y = 85

    for block in list(filter(lambda i: blocks[i]['placeable'], blocks.keys())):
        if x <= mouse[0] <= x + 42 and y <= mouse[1] <= y + 42:
            surface.fill((255, 255, 255), (x - 5, y - 5, 52, 52))

        surface.blit(helper.draw_texture(blocks[block]['texture']), (x, y))
        x += 52

        if x >= 1040:
            x = 50
            y += 52


    x = 50
    y = 85

    for block in list(filter(lambda i: blocks[i]['placeable'], blocks.keys())):
        if x <= mouse[0] <= x + 42 and y <= mouse[1] <= y + 42:
            text = pygame.font.Font("./assets/font/main.ttf", 20).render(blocks[block]['name'], False, (0, 0, 0), (255, 255, 255))
            surface.blit(text, (x - (text.get_width() / 2) + 21, y - text.get_height() - 5))

        x += 52

        if x >= 1040:
            x = 50
            y += 52

    return surface

def click(mouse, screen, picker, selected_block):
    x = 50
    y = 85

    for block in list(filter(lambda i: blocks[i]['placeable'], blocks.keys())):
        if x <= mouse[0] <= x + 42 and y <= mouse[1] <= y + 42:
            audio.play_sfx("action")
            selected_block = block
            picker = False

        x += 52

        if x >= 1040:
            x = 50
            y += 52

    return mouse, screen, picker, selected_block