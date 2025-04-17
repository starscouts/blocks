import pygame
import constants

def show_debug(clock, extended=False):
    screen = pygame.display.get_surface()

    if extended:
        accelerates = []
        info = pygame.display.Info()
    
        if info.hw == 1:
            accelerates.append("HARDWARE")
        if info.blit_hw == 1:
            accelerates.append("HW_BLIT")
        if info.blit_hw_CC == 1:
            accelerates.append("HW_BLIT_CK")
        if info.blit_hw_A == 1:
            accelerates.append("HW_BLIT_RGBA")
        if info.blit_sw == 1:
            accelerates.append("BLIT")
        if info.blit_sw_CC == 1:
            accelerates.append("BLIT_CK")
        if info.blit_sw_A == 1:
            accelerates.append("BLIT_RGBA")
    
        width = screen.get_size()[0]
        height = width / (16/9)
    
        if width > screen.get_size()[0] or height > screen.get_size()[1]:
            height = screen.get_size()[1]
            width = height * (16/9)
    
        offset_x = screen.get_size()[0] / 2 - width / 2
        offset_y = screen.get_size()[1] / 2 - height / 2
        scaling = ((width / 1280) + (height / 720)) / 2
    
        text = [
            f"Blocks {constants.VERSION}, Pygame {pygame.version.ver}, SDL {pygame.version.SDL}",
            f"{str(round(clock.get_fps()))} FPS",
            f"",
            f"Graphics:",
            f"    Driver: {pygame.display.get_driver()}, VRAM: {info.video_mem} MB, {info.bitsize}bit color",
            f"    Acceleration: {','.join(accelerates)}",
            f"    Window: {pygame.display.get_window_size()[0]}x{pygame.display.get_window_size()[1]}, Scaling factor: {round(scaling, 3)}x",
            f"",
            f"Audio:",
            f"    Mixer: {pygame.mixer.get_sdl_mixer_version()}",
            f"    Channels:"
        ]
    
        for i in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(i)
            txt = "        " + str(i) + ": [" + str(round(channel.get_volume(), 3)) + "] "
    
            if channel.get_busy():
                sound = channel.get_sound()
                txt += hex(id(sound)) + " (" + str(round(sound.get_length(), 3)) + ")"
            else:
                txt += " <idle>"
    
            text.append(txt)
    else:
        text = [f"{str(round(clock.get_fps()))} FPS"]

    for i in range(len(text)):
        screen.blit(pygame.font.SysFont("Arial", 14).render(text[i], True, (255, 255, 255), (0, 0, 0)), (5, screen.get_size()[1] - 20 - ((len(text) - 1 - i) * 15)))
