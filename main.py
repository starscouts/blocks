import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import traceback
import datetime
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import pygame

import sys
sys.path.append("./src")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE | pygame.HWSURFACE | pygame.HWACCEL | pygame.DOUBLEBUF, vsync=True)

from src import window
pygame.mixer.pre_init(44100, 16, 2, 4096)
window.init()
pygame.init()

screen.fill("black")
pygame.display.flip()

focused = True
running = True

index = 0

from src import audio, loader, menu
played_audio = False
showing_load = True
pygame.font.init()

while running:
    try:
        screen.fill("black")

        pygame.event.set_allowed([pygame.WINDOWRESIZED, pygame.WINDOWEXPOSED, pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWFOCUSLOST, pygame.WINDOWFOCUSGAINED, pygame.WINDOWMINIMIZED, pygame.QUIT])
        for event in pygame.event.get():
            if event.type == pygame.WINDOWFOCUSLOST:
                focused = False
            if event.type == pygame.WINDOWFOCUSGAINED:
                focused = True
            if event.type == pygame.QUIT:
                running = False

        if not played_audio:
            audio.play_intro()
            played_audio = True

        if showing_load:
            if index <= 60:
                screen.blit(pygame.transform.scale(loader.draw_texture(index), (180, 180)), (1280 / 2 - 180 / 2, 720 / 2 - 180 / 2))

            index += 1

            if index > 70:
                showing_load = False

            if focused:
                pygame.display.flip()

            clock.tick(25)
        else:
            loader.unload_intro()
            import helper
            helper.get_data_path()
            menu.show(screen)
            break
    except Exception as e:
        pygame.mixer.music.load("./assets/sounds/gui/error.ogg")
        pygame.mixer.music.play()
        pygame.mouse.set_visible(True)

        running = True

        if pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).pause()

        screen.fill((0, 0, 0))

        img = pygame.image.load("./assets/textures/crash.png").convert_alpha()
        img.convert()

        screen.blit(pygame.transform.scale(img, (84, 84)), (100, 100))

        message = e.message if hasattr(e, 'message') else str(e)
        code = ("".join([hex(ord(i)).split("x")[1] for i in message]) + "00000000").upper()
        screen.blit(pygame.font.Font("./assets/font/main.ttf", 20).render("An error has occurred and the game has stopped.", False, (255, 255, 255)), (200, 124))
        screen.blit(pygame.font.Font("./assets/font/main.ttf", 20).render("Error code: 0x" + code[0:8], False, (255, 255, 255)), (199, 144))

        if focused:
            pygame.display.flip()

        print(traceback.format_exc())

        try:
            with open(helper.get_data_path() + "/crash_reports/" + datetime.datetime.now().isoformat().replace(":", "-") + ".txt", "w") as f:
                f.write(traceback.format_exc())
        except Exception:
            print(traceback.format_exc())

        while running:
            pygame.event.set_allowed([pygame.WINDOWRESIZED, pygame.WINDOWEXPOSED, pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWFOCUSLOST, pygame.WINDOWFOCUSGAINED, pygame.WINDOWMINIMIZED, pygame.QUIT])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                clock.tick(1)

pygame.quit()
