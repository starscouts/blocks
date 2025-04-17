import os.path

import pygame
import helper
import audio
import save
import constants
import debug

clock = pygame.time.Clock()

def show(screen):
    running = True
    focused = True
    opacity = 0
    audio.play_menu(True)

    while running:
        pygame.event.set_allowed([pygame.WINDOWRESIZED, pygame.WINDOWEXPOSED, pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWFOCUSLOST, pygame.WINDOWFOCUSGAINED, pygame.WINDOWMINIMIZED, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.QUIT])
        for event in pygame.event.get():
            if event.type == pygame.WINDOWFOCUSLOST:
                focused = False
            if event.type == pygame.WINDOWFOCUSGAINED:
                focused = True
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                mouse = helper.get_real_mouse(screen)
                print(mouse)

                if left:
                    if 45 < mouse[0] < 195 and 40 < mouse[1] < 70:
                        audio.play_sfx("action")
                        print("New game")
                        screen.fill("black")
                        canvas = pygame.Surface((1280, 720))
                        canvas.fill("black")

                        width = screen.get_size()[0]
                        height = width / (16/9)

                        if width > screen.get_size()[0] or height > screen.get_size()[1]:
                            height = screen.get_size()[1]
                            width = height * (16/9)

                        run = True
                        done = False
                        text = ""
                        quit = False

                        while run and not done:
                            canvas.fill("black")

                            pygame.event.set_allowed([pygame.WINDOWRESIZED, pygame.WINDOWEXPOSED, pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWFOCUSLOST, pygame.WINDOWFOCUSGAINED, pygame.WINDOWMINIMIZED, pygame.QUIT, pygame.KEYDOWN])
                            for event in pygame.event.get():
                                if event.type == pygame.WINDOWFOCUSLOST:
                                    focused = False
                                if event.type == pygame.WINDOWFOCUSGAINED:
                                    focused = True
                                if event.type == pygame.QUIT:
                                    run = False
                                    quit = True
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        run = False
                                    elif event.key == pygame.K_RETURN:
                                        text = text.strip()

                                        for i in ["con", "prn", "aux", "nul",
                                                  "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
                                                  "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"]:
                                            if text.lower() == i or text.startswith(i + ".") or text.endswith("." + i):
                                                text = ""

                                        if text.strip() != "" and not os.path.exists(helper.get_data_path() + "/saves/" + text):
                                            done = True
                                        elif os.path.exists(helper.get_data_path() + "/saves/" + text):
                                            text = ""
                                        else:
                                            text = text.strip()
                                    elif event.key == pygame.K_BACKSPACE:
                                        text = text[:-1]
                                    else:
                                        if event.unicode not in ["/", "\\", "<", ">", ":", "\"", "'", "|", "?", "*"] and len(text) < 60:
                                            text += event.unicode

                            text_surf = helper.text(text + "|", 20, (255, 255, 255))
                            canvas.blit(text_surf, (50, 75))
                            canvas.blit(helper.text("Enter world name:", 20, (255, 255, 255)), (50, 50))

                            scaled_win = pygame.transform.scale(canvas, (width, height))
                            screen.blit(scaled_win, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))
                            if focused:
                                debug.show_debug(clock)
                                pygame.display.flip()

                            clock.tick(25)

                        if quit:
                            pygame.quit()
                        elif done:
                            audio.stop(1)
                            audio.play_sfx("menu")

                            canvas.fill("black")
                            canvas.blit(helper.text("Generating world...", 20, (255, 255, 255)), (50, 50))

                            scaled_win = pygame.transform.scale(canvas, (width, height))
                            screen.blit(scaled_win, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))
                            debug.show_debug(clock)
                            pygame.display.flip()

                            audio.wait_for_sfx()

                            import game
                            game.run(screen, helper.get_data_path() + "/saves/" + text)

                            return
                        else:
                            audio.play_sfx("back")
                    elif 45 < mouse[0] < 205 and 40+25 < mouse[1] < 70+25:
                        audio.play_sfx("action")
                        print("Load game")
                        screen.fill("black")
                        canvas = pygame.Surface((1280, 720))
                        canvas.fill("black")

                        width = screen.get_size()[0]
                        height = width / (16/9)

                        if width > screen.get_size()[0] or height > screen.get_size()[1]:
                            height = screen.get_size()[1]
                            width = height * (16/9)

                        run = True
                        done = False
                        quit = False
                        world_name = ""

                        saves = list(filter(lambda x: not x.startswith(".") and os.path.exists(helper.get_data_path() + "/saves/" + x + "/level.dat"), os.listdir(helper.get_data_path() + "/saves")))

                        while run and not done:
                            canvas.fill("black")

                            pygame.event.set_allowed([pygame.WINDOWRESIZED, pygame.WINDOWEXPOSED, pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWFOCUSLOST, pygame.WINDOWFOCUSGAINED, pygame.WINDOWMINIMIZED, pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])
                            for event in pygame.event.get():
                                if event.type == pygame.WINDOWFOCUSLOST:
                                    focused = False
                                if event.type == pygame.WINDOWFOCUSGAINED:
                                    focused = True
                                if event.type == pygame.QUIT:
                                    run = False
                                    quit = True
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    cursor = helper.get_real_mouse(screen)

                                    for i in range(len(saves)):
                                        save_name = saves[i]

                                        if 45 < cursor[0] < 550 and 65+25*i < cursor[1] < 95+25*i:
                                            print(save_name)
                                            world_name = save_name
                                            done = True
                                            break

                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        run = False

                            canvas.blit(helper.text("Select a world to load:", 20, (255, 255, 255)), (50, 50))

                            last_i = 0

                            for i in range(len(saves)):
                                save_name = saves[i]
                                canvas.blit(helper.text(save_name, 20, (255, 255, 255)), (75, 75 + (25 * i)))
                                last_i = i

                            canvas.blit(helper.text("Notice:", 20, (255, 255, 255)), (50, 75 + (25 * (last_i + 2))))
                            canvas.blit(helper.text("Worlds from Blocks 0.1a are not compatible and", 20, (255, 255, 255)), (75, 75 + (25 * (last_i + 3))))
                            canvas.blit(helper.text("do not show up here.", 20, (255, 255, 255)), (75, 75 + (25 * (last_i + 4))))
                            canvas.blit(helper.text("Worlds from Blocks 0.2a are not compatible and", 20, (255, 255, 255)), (75, 75 + (25 * (last_i + 5))))
                            canvas.blit(helper.text("will crash the game.", 20, (255, 255, 255)), (75, 75 + (25 * (last_i + 6))))

                            scaled_win = pygame.transform.scale(canvas, (width, height))
                            screen.blit(scaled_win, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))
                            if focused:
                                debug.show_debug(clock)
                                pygame.display.flip()

                            clock.tick(25)
                        if quit:
                            pygame.quit()
                        elif done:
                            audio.stop(1)
                            audio.play_sfx("menu")

                            canvas.fill("black")
                            canvas.blit(helper.text("Loading world...", 20, (255, 255, 255)), (50, 50))

                            scaled_win = pygame.transform.scale(canvas, (width, height))
                            screen.blit(scaled_win, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))
                            debug.show_debug(clock)
                            pygame.display.flip()

                            loaded = save.load_world(helper.get_data_path() + "/saves/" + world_name)

                            if loaded['version'] != constants.VERSION:
                                print("WARNING: World was last loaded in a different version.")

                            audio.wait_for_sfx()

                            import game
                            game.run(screen, helper.get_data_path() + "/saves/" + world_name)

                            return
                        else:
                            audio.play_sfx("back")
                    elif 45 < mouse[0] < 125 and 40+25*2 < mouse[1] < 70+25*2:
                    #    audio.play_sfx("action")
                    #    print("Settings")
                    #elif 45 < mouse[0] < 90 and 40+25*3 < mouse[1] < 70+25*3:
                        audio.play_sfx("action")
                        audio.wait_for_sfx()
                        print("Exit")
                        running = False

            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        canvas = pygame.Surface((1280, 720))
        canvas.fill("red")

        width = screen.get_size()[0]
        height = width / (16/9)

        if width > screen.get_size()[0] or height > screen.get_size()[1]:
            height = screen.get_size()[1]
            width = height * (16/9)

        canvas.blit(helper.text("Start new game", 20, (255, 255, 255)), (50, 50))
        canvas.blit(helper.text("Load saved game", 20, (255, 255, 255)), (50, 75))
        #canvas.blit(helper.text("Settings", 20, (255, 255, 255)), (50, 100))
        #canvas.blit(helper.text("Exit", 20, (255, 255, 255)), (50, 125))
        canvas.blit(helper.text("Exit", 20, (255, 255, 255)), (50, 100))

        scaled_win = pygame.transform.scale(canvas, (width, height))

        if opacity >= 1:
            result = scaled_win
        else:
            result = helper.transparent(scaled_win, opacity)

        screen.blit(result, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))

        audio.play_menu()
        if focused:
            debug.show_debug(clock)
            pygame.display.flip()

        if opacity < 1:
            opacity += 1/30

        if opacity >= 1:
            opacity = 1

        clock.tick(25)
