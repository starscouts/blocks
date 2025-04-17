import pygame

import helper
import audio
import save

def show():
    surface = pygame.Surface((1280, 720))
    surface.fill((0, 0, 0, 128))

    surface.blit(helper.text("Back to game", 20, (255, 255, 255)), (50, 50))
    surface.blit(helper.text("Save and quit", 20, (255, 255, 255)), (50, 75))

    return surface

def click(mouse, screen, paused, keep, save_data, regions):
    if 45 < mouse[0] < 195 and 40 < mouse[1] < 70:
        audio.play_sfx("action")
        print("Back")
        audio.play_sfx("back")
        audio.unpause_music()
        pygame.mouse.set_visible(True)
        paused = False
    elif 45 < mouse[0] < 205 and 40+25 < mouse[1] < 70+25:
        audio.play_sfx("action")
        print("Save game")
        save_and_quit(screen, save_data, regions)
        keep = False
        import menu
        menu.show(screen)

    return mouse, screen, paused, keep

def save_and_quit(screen, path, regions, sfx=True):
    if sfx:
        audio.play_sfx("save")

    canvas = pygame.Surface((1280, 720))
    canvas.fill("black")

    width = screen.get_size()[0]
    height = width / (16/9)

    if width > screen.get_size()[0] or height > screen.get_size()[1]:
        height = screen.get_size()[1]
        width = height * (16/9)

    canvas.blit(helper.text("Saving world...", 20, (255, 255, 255)), (50, 50))

    scaled_win = pygame.transform.scale(canvas, (width, height))
    screen.blit(scaled_win, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))

    pygame.display.flip()
    audio.stop(1)

    if sfx:
        audio.wait_for_sfx()

    save.save_world(path, regions)