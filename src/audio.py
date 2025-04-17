import pygame
import random

enable_audio = True

try:
    pygame.mixer.init()
except pygame.error:
    print("WARNING: Failed to initialize DSP mixer.")
    enable_audio = False

pygame.mixer.set_num_channels(3)

pygame.mixer.stop()

intro = pygame.mixer.Sound("./assets/sounds/intro.mp3")
menu = pygame.mixer.Sound("./assets/music/menu.mp3")

bgm = [
    pygame.mixer.Sound("./assets/music/bgm1.mp3"),
    pygame.mixer.Sound("./assets/music/bgm2.mp3"),
    pygame.mixer.Sound("./assets/music/bgm3.mp3"),
    pygame.mixer.Sound("./assets/music/bgm4.mp3"),
    pygame.mixer.Sound("./assets/music/bgm5.mp3")
]

sfx = {
    "action": [pygame.mixer.Sound("./assets/sounds/gui/action.ogg")],
    "back": [pygame.mixer.Sound("./assets/sounds/gui/back.ogg")],
    "menu": [pygame.mixer.Sound("./assets/sounds/gui/menu.ogg")],
    "save": [pygame.mixer.Sound("./assets/sounds/gui/save.ogg")],
    "glass": [
        pygame.mixer.Sound("./assets/sounds/game/block_glass_1.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_glass_2.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_glass_3.ogg")
    ],
    "grass": [
        pygame.mixer.Sound("./assets/sounds/game/block_grass_1.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_grass_2.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_grass_3.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_grass_4.ogg")
    ],
    "stone": [
        pygame.mixer.Sound("./assets/sounds/game/block_stone_1.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_stone_2.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_stone_3.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_stone_4.ogg")
    ],
    "wood": [
        pygame.mixer.Sound("./assets/sounds/game/block_wood_1.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_wood_2.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_wood_3.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_wood_4.ogg")
    ],
    "cloth": [
        pygame.mixer.Sound("./assets/sounds/game/block_cloth_1.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_cloth_2.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_cloth_3.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/block_cloth_4.ogg")
    ],
    "none": [
        pygame.mixer.Sound("./assets/sounds/game/none_1.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/none_2.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/none_3.ogg"),
        pygame.mixer.Sound("./assets/sounds/game/none_4.ogg")
    ]
}

def play_intro():
    if not enable_audio:
        return
    pygame.mixer.Channel(0).play(intro)

def play_music():
    if not enable_audio:
        return
    if not pygame.mixer.Channel(1).get_busy():
        pygame.mixer.Channel(1).set_volume(0.5)
        pygame.mixer.Channel(1).play(random.choice(bgm))

def play_menu(force=False):
    if not enable_audio:
        return
    if not pygame.mixer.Channel(1).get_busy() or force:
        pygame.mixer.Channel(1).set_volume(0.5)
        pygame.mixer.Channel(1).play(menu)

def stop(channel=1):
    if not enable_audio:
        return
    pygame.mixer.Channel(channel).stop()

def pause_music():
    if not enable_audio:
        return
    pygame.mixer.Channel(1).pause()

def unpause_music():
    if not enable_audio:
        return
    pygame.mixer.Channel(1).unpause()

def play_sfx(id):
    if not enable_audio:
        return
    pygame.mixer.Channel(2).play(random.choice(sfx[id]))

def wait_for_sfx():
    if not enable_audio:
        return
    while pygame.mixer.Channel(2).get_busy():
        pass
