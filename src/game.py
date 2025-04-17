import pygame

from blocks import blocks as block_list
import audio
import zoom as zoom_util
import picker as picker_ui
import display
import pause
import save
import time
import helper

clock = pygame.time.Clock()

def run(screen, save_data):
    global clock

    first = True
    focused = True
    canvas = pygame.Surface((1280, 720))
    running = True
    zoom = (1280.0, 720.0)
    offset = (0, 0)
    mouse = (-1, -1)
    block_coordinates = (-1, -1)
    need_update_world = True
    world = pygame.Surface((1280, 720))
    paused = False
    picker = False
    screen_blocks = []
    selected_block = "stone"
    loaded_chunks = []
    pressed_key = None
    last_key_repeat = 5

    save.save_world(save_data, loaded_chunks)

    display.opacity = 0

    last = time.time()

    if time.time() - last >= 300:
        save.save_world(save_data, loaded_chunks)
        last = time.time()

    while running:
        if not paused:
            audio.play_music()

        pygame.event.set_allowed([pygame.WINDOWRESIZED, pygame.WINDOWEXPOSED, pygame.WINDOWENTER, pygame.WINDOWLEAVE, pygame.WINDOWFOCUSLOST, pygame.WINDOWFOCUSGAINED, pygame.WINDOWMINIMIZED, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT])
        for event in pygame.event.get():
            if event.type == pygame.WINDOWFOCUSLOST:
                focused = False
            if event.type == pygame.WINDOWFOCUSGAINED:
                focused = True
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(paused or picker)
                mouse = helper.get_real_mouse(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                print(helper.get_real_mouse(screen))

                if paused:
                    if left:
                        mouse, screen, paused, keep = pause.click(mouse, screen, paused, True, save_data, loaded_chunks)
                        if not keep:
                            return
                elif picker:
                    if left:
                        mouse, screen, picker, selected_block = picker_ui.click(mouse, screen, picker, selected_block)
                else:
                    if left:
                        for i in range(len(screen_blocks)):
                            if screen_blocks[i][0] == block_coordinates[0] and screen_blocks[i][1] == block_coordinates[1]:
                                chunk = None

                                for chunk_metadata in helper.get_chunk_regions(loaded_chunks):
                                    if chunk_metadata['range'][0] <= screen_blocks[i][4] <= chunk_metadata['range'][2] and chunk_metadata['range'][1] <= screen_blocks[i][5] <= chunk_metadata['range'][3]:
                                        chunk_x = int(chunk_metadata['file'].split(",")[0])
                                        chunk_y = int(chunk_metadata['file'].split(",")[1].split(".")[0])

                                        chunk_is_loaded = False

                                        if len(loaded_chunks) - 1 >= chunk_x:
                                            if len(loaded_chunks[chunk_x]) - 1 >= chunk_y:
                                                if loaded_chunks[chunk_x][chunk_y] is not None:
                                                    chunk_is_loaded = True

                                        if chunk_is_loaded:
                                            chunk = loaded_chunks[chunk_x][chunk_y]
                                        else:
                                            chunk = save.get_chunk(save_data, (chunk_x, chunk_y))

                                            while len(loaded_chunks) - 1 <= chunk_x:
                                                loaded_chunks.append([])

                                            while len(loaded_chunks[chunk_x]) - 1 <= chunk_y:
                                                loaded_chunks[chunk_x].append(None)

                                            loaded_chunks[chunk_x][chunk_y] = chunk
                                        break

                                if chunk is not None:
                                    if len(chunk) - 1 < screen_blocks[i][3] + 1 < 65:
                                        chunk.append([["air" for _ in range(16)] for _ in range(16)])

                                    target_x = screen_blocks[i][6]
                                    target_y = screen_blocks[i][3] + 1
                                    target_z = screen_blocks[i][7]
                                    target_x_changed = False
                                    target_z_changed = False

                                    if abs(mouse[0] - block_coordinates[0]) <= 12:
                                        target_x = screen_blocks[i][6]
                                        target_y = screen_blocks[i][3]
                                        target_z = screen_blocks[i][7] - 1
                                        target_z_changed = True
                                    elif abs(mouse[0] - block_coordinates[0]) >= 30:
                                        target_x = screen_blocks[i][6] - 1
                                        target_y = screen_blocks[i][3]
                                        target_z = screen_blocks[i][7]
                                        target_x_changed = True

                                    if len(chunk) - 1 >= target_y and len(chunk[target_y]) - 1 >= target_x and len(chunk[target_y][target_x]) - 1 >= target_z and chunk[target_y][target_x][target_z] == "air" and chunk[target_y][target_x][target_z] != selected_block:
                                        audio.play_sfx(block_list[selected_block]['sounds'][0])
                                        chunk[target_y][target_x][target_z] = selected_block
                                        need_update_world = True
                                    else:
                                        print("Cannot place block at " + str(target_x) + ", " + str(target_y) + ", " + str(target_z))

                                break
                    elif right:
                        for i in range(len(screen_blocks)):
                            if screen_blocks[i][0] == block_coordinates[0] and screen_blocks[i][1] == block_coordinates[1] and screen_blocks[i][2] != "bedrock":
                                chunk = None

                                for chunk_metadata in helper.get_chunk_regions(loaded_chunks):
                                    if chunk_metadata['range'][0] <= screen_blocks[i][4] <= chunk_metadata['range'][2] and chunk_metadata['range'][1] <= screen_blocks[i][5] <= chunk_metadata['range'][3]:
                                        chunk_x = int(chunk_metadata['file'].split(",")[0])
                                        chunk_y = int(chunk_metadata['file'].split(",")[1].split(".")[0])

                                        chunk_is_loaded = False

                                        if len(loaded_chunks) - 1 >= chunk_x:
                                            if len(loaded_chunks[chunk_x]) - 1 >= chunk_y:
                                                if loaded_chunks[chunk_x][chunk_y] is not None:
                                                    chunk_is_loaded = True

                                        if chunk_is_loaded:
                                            chunk = loaded_chunks[chunk_x][chunk_y]
                                        else:
                                            chunk = save.get_chunk(save_data, (chunk_x, chunk_y))

                                            while len(loaded_chunks) - 1 <= chunk_x:
                                                loaded_chunks.append([])

                                            while len(loaded_chunks[chunk_x]) - 1 <= chunk_y:
                                                loaded_chunks[chunk_x].append(None)

                                            loaded_chunks[chunk_x][chunk_y] = chunk
                                        break

                                if chunk is not None:
                                    if block_list[screen_blocks[i][2]]:
                                        audio.play_sfx(block_list[screen_blocks[i][2]]['sounds'][1])

                                    chunk[screen_blocks[i][3]][screen_blocks[i][6]][screen_blocks[i][7]] = "air"
                                    need_update_world = True

                                break

                        if not need_update_world:
                            audio.play_sfx("none")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if picker:
                        clock.tick(60)
                        audio.play_sfx("back")
                        picker = False
                    else:
                        paused = not paused
                        if paused:
                            clock.tick(25)
                            audio.play_sfx("menu")
                            audio.pause_music()
                        else:
                            clock.tick(60)
                            audio.play_sfx("back")
                            audio.unpause_music()
                        pygame.mouse.set_visible(paused)
                elif pressed_key == pygame.K_e:
                    picker = not picker
                    if picker:
                        audio.play_sfx("menu")
                    else:
                        audio.play_sfx("back")
                    pygame.mouse.set_visible(paused)
                else:
                    pressed_key = event.key
            if event.type == pygame.KEYUP:
                pressed_key = None
                last_key_repeat = 5
            if event.type == pygame.QUIT:
                pause.save_and_quit(screen, save_data, loaded_chunks, False)
                running = False

        if pressed_key is not None and last_key_repeat >= 5:
            last_key_repeat = 0

            if pressed_key == pygame.K_w or pressed_key == pygame.K_z:
                offset = zoom_util.offset_up(offset)
                need_update_world = True
            if pressed_key == pygame.K_s:
                offset = zoom_util.offset_down(offset)
                need_update_world = True
            if pressed_key == pygame.K_q or pressed_key == pygame.K_a:
                offset = zoom_util.offset_left(offset)
                need_update_world = True
            if pressed_key == pygame.K_d:
                offset = zoom_util.offset_right(offset)
                need_update_world = True
            if pressed_key == pygame.K_o:
                zoom = zoom_util.zoom_in(zoom)
                need_update_world = True
            if pressed_key == pygame.K_l:
                zoom = zoom_util.zoom_out(zoom)
                need_update_world = True
            if pressed_key == pygame.K_p:
                zoom, offset = zoom_util.zoom_reset()
                need_update_world = True

        if pressed_key is not None:
            last_key_repeat += 1

        canvas, screen, need_update_world, world, mouse, loaded_chunks, zoom, offset, block_coordinates, paused, screen_blocks, selected_block, picker, blocks, save_data, focused, clock = display.draw(canvas, screen, need_update_world, world, mouse, loaded_chunks, zoom, offset, block_coordinates, paused, screen_blocks, selected_block, picker, save_data, focused, clock)

        clock.tick(60)
