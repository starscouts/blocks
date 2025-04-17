from blocks import blocks
import pygame
from math import floor
from sys import platform
from pathlib import Path
import os

texture_map = pygame.image.load('./assets/textures/texture_atlas.png')
controls_map = pygame.image.load('./assets/textures/controls.png')

def get_data_path():
    path = str(Path.home()) + "/.blocks"

    if platform == "darwin":
        path = str(Path.home()) + "/Library/Application Support/Blocks"
    elif platform == "win32":
        path = str(Path.home()).replace("\\", "/") + "/.blocks"

    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(path + "/saves"):
        os.mkdir(path + "/saves")

    if not os.path.exists(path + "/crash_reports"):
        os.mkdir(path + "/crash_reports")

    return path

def transparent(surface, percentage):
    screen = pygame.Surface((1280, 720))
    screen.fill("black")
    screen.blit(surface, (0, 0))

    surface2 = pygame.Surface((1280, 720))
    surface2.fill((0, 0, 0, 255*(1-percentage)))
    screen.blit(pygame.Surface.convert_alpha(surface2), (0, 0))

    return screen

def text(text, size, color):
    return pygame.Surface.convert_alpha(pygame.font.Font("./assets/font/main.ttf", size).render(text, False, color))

def get_block_texture(block):
    return blocks[block]['texture']

def draw_texture(id):
    x = 0
    y = 0

    for i in range(id):
        x += 42

        if x >= 420:
            x = 0
            y += 42

    return texture_map.subsurface((x, y, 42, 42))

def draw_control(id):
    if id < 10:
        pos = (17 * id, 0)
    else:
        pos = (17 * (id - (floor(((id + 1) / 10) - 1) * 10)), 17 * (floor(((id + 1) / 10) - 1)))

    return pygame.Surface.convert_alpha(controls_map.subsurface((pos[0], pos[1], 17, 17)))

def get_chunk_regions(chunks):
    data = []

    for x in range(len(chunks)):
        for y in range(len(chunks)):
            data.append({
                "file": str(x) + "," + str(y) + ".bcr",
                "range": (16 * x, 16 * y, 15 + 16 * x, 15 + 16 * y)
            })

    return data

def get_real_mouse(screen):
    width = screen.get_size()[0]
    height = width / (16/9)

    if width > screen.get_size()[0] or height > screen.get_size()[1]:
        height = screen.get_size()[1]
        width = height * (16/9)

    offset_x = screen.get_size()[0] / 2 - width / 2
    offset_y = screen.get_size()[1] / 2 - height / 2
    scaling = ((width / 1280) + (height / 720)) / 2

    pos = pygame.mouse.get_pos()

    return (int((pos[0] - offset_x) / scaling), int((pos[1] - offset_y) / scaling))
