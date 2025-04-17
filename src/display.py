import pygame

import helper
import pause
import picker as picker_ui
import time
import save
import debug

opacity = 0

def draw(canvas, screen, need_update_world, world, mouse, loaded_chunks, zoom, offset, block_coordinates, paused, screen_blocks, selected_block, picker, save_data, focused, clock):
    blocks = []

    start = time.time()
    timings = {}
    global opacity
    canvas.fill("red")

    width = screen.get_size()[0]
    height = width / (16/9)

    if width > screen.get_size()[0] or height > screen.get_size()[1]:
        height = screen.get_size()[1]
        width = height * (16/9)

    world_display = pygame.Surface((1280, 720))
    needed_update_world = need_update_world

    if need_update_world:
        screen_blocks = []
        world.fill("gray")

        tstart = time.time()

        chunks_to_display = []
        print(chunks_to_display)

        for x in range(len(loaded_chunks)):
            for y in range(len(loaded_chunks[x])):
                if loaded_chunks[x][y] is not None:
                    if (x, y) not in chunks_to_display:
                        save.save_chunk(save_data, str(x) + "," + str(y) + ".bcr", loaded_chunks[x][y])
                        loaded_chunks[x][y] = None

        chunk_x = 0

        for _ in range(8):
            chunk_y = 0
            display_status = []

            for _ in range(8):
                displayed = False
                coords = []

                for layer in range(1):
                    for height in range(15, -1, -1):
                        for width in range(15, -1, -1):
                            coords.append((offset[0] + (chunk_x * 336) - (chunk_y * 333) + 500 + (21 * width) - (21 * height), offset[1] + (chunk_x * 193) + (chunk_y * 222) + 500 - (13 * layer) - (14 * width) - (12 * height)))

                for coord in coords:
                    if 0 < coord[0] < 1280 and 0 < coord[1] < 720:
                        displayed = True

                display_status.append(displayed)
                if displayed:
                    chunks_to_display.append((chunk_x, chunk_y))
                chunk_y += 1
            chunk_x += 1

        print(chunks_to_display)

        for chunk_coords in chunks_to_display:
            chunk_x = chunk_coords[0]
            chunk_y = chunk_coords[1]

            chunk_is_loaded = False

            if len(loaded_chunks) - 1 >= chunk_x:
                if len(loaded_chunks[chunk_x]) - 1 >= chunk_y:
                    if loaded_chunks[chunk_x][chunk_y] is not None:
                        chunk_is_loaded = True

            if chunk_is_loaded:
                blocks = loaded_chunks[chunk_x][chunk_y]
            else:
                blocks = save.get_chunk(save_data, (chunk_x, chunk_y))

                while len(loaded_chunks) - 1 <= chunk_x:
                    loaded_chunks.append([])
                    
                while len(loaded_chunks[chunk_x]) - 1 <= chunk_y:
                    loaded_chunks[chunk_x].append(None)

                loaded_chunks[chunk_x][chunk_y] = blocks

            for layer in range(len(blocks)):
                for height in range(len(blocks[layer]) - 1, -1, -1):
                    if len(blocks[layer][height]) == len(list(filter(lambda i: i == "air", blocks[layer][height]))):
                        continue

                    for width in range(len(blocks[layer][height]) - 1, -1, -1):
                        if blocks[layer][height][width] != "air":
                            x = offset[0] + (chunk_x * 336) - (chunk_y * 333) + 500 + (21 * width) - (21 * height)
                            y = offset[1] + (chunk_x * 193) + (chunk_y * 222) + 500 - (13 * layer) - (14 * width) - (12 * height)
                            world.blit(helper.draw_texture(helper.get_block_texture(blocks[layer][height][width])), (x, y))

            for layer in range(len(blocks) - 1, -1, -1):
                for height in range(len(blocks[layer]) - 1, -1, -1):
                    if len(blocks[layer][height]) == len(list(filter(lambda i: i == "air", blocks[layer][height]))):
                        continue

                    for width in range(len(blocks[layer][height]) - 1, -1, -1):
                        if blocks[layer][height][width] != "air":
                            x = offset[0] + (chunk_x * 336) - (chunk_y * 333) + 500 + (21 * width) - (21 * height)
                            y = offset[1] + (chunk_x * 193) + (chunk_y * 222) + 500 - (13 * layer) - (14 * width) - (12 * height)
                            screen_blocks.append((x, y, blocks[layer][height][width], layer, height + (chunk_x * 16), width + (chunk_y * 16), height, width))

        timings['draw_map'] = (time.time() - tstart) * 1000
        tstart = time.time()
        need_update_world = False

    tstart = time.time()
    world_display.blit(world, (0, 0))
    timings['screen_display_world'] = (time.time() - tstart) * 1000

    screen_blocks = list(sorted(screen_blocks, key=lambda k: -k[3]))

    tstart = time.time()

    if mouse[0] > -1 and mouse[1] > -1 and pygame.mouse.get_focused() and not paused and not picker:
        cursor_x = original_cursor_x = mouse[0] - 42 / 2
        cursor_y = original_cursor_y = mouse[1] - 42 / 2
        cursor_changed = False

        for i in range(len(screen_blocks)):
            block = screen_blocks[i]

            if block[0] <= mouse[0] <= block[0] + 42 and block[1] <= mouse[1] <= block[1] + 42 and block[2] != "bedrock" and block[2] != "air":
                cursor_x = block[0]
                cursor_y = block[1]
                cursor_changed = True
                break

        if cursor_changed:
            world_display.blit(helper.draw_texture(5), (cursor_x, cursor_y))
            block_coordinates = (cursor_x, cursor_y)
        else:
            block_coordinates = (-1, -1)

        world_display.blit(helper.draw_texture(2), (original_cursor_x + 42 / 2, original_cursor_y + 42 / 2))

    timings['process_mouse'] = (time.time() - tstart) * 1000
    tstart = time.time()

    x = 1280 / 2 - zoom[0] / 2
    y = 720 / 2 - zoom[1] / 2

    if x < 0:
        x = 0

    if y < 0:
        y = 0

    if x + zoom[0] > 1280:
        x = 0

    if y + zoom[1] > 720:
        y = 0

    canvas.blit(pygame.transform.scale(world_display.subsurface(x, y, zoom[0], zoom[1]), (1280, 720)), (0, 0))
    timings['screen_display_world_zoomed'] = (time.time() - tstart) * 1000
    tstart = time.time()

    canvas.blit(pygame.transform.scale(helper.draw_control(79), (34, 34)), (10, 10))
    canvas.blit(helper.text("Pause", 20, (255, 255, 255)), (54, 20))
    canvas.blit(pygame.transform.scale(pygame.Surface.convert_alpha(helper.draw_texture(0)), (84, 84)), (1191, 631))
    timings['hud_static'] = (time.time() - tstart) * 1000
    tstart = time.time()

    canvas.blit(pygame.Surface.convert_alpha(helper.draw_texture(helper.get_block_texture(selected_block))), (1228, 10))
    canvas.blit(pygame.transform.scale(helper.draw_control(4), (34, 34)), (1184, 15))

    timings['hud_picker'] = (time.time() - tstart) * 1000
    tstart = time.time()

    if paused:
        canvas.blit(pause.show(), (0, 0))

    if picker:
        canvas.blit(picker_ui.show(mouse), (0, 0))

    timings['hud_gui'] = (time.time() - tstart) * 1000
    tstart = time.time()

    scaled_win = pygame.transform.scale(canvas, (width, height))

    if opacity >= 1:
        result = scaled_win
    else:
        result = helper.transparent(scaled_win, opacity)

    screen.blit(result, (screen.get_size()[0] / 2 - width / 2, screen.get_size()[1] / 2 - height / 2))
    timings['screen_display_final'] = (time.time() - tstart) * 1000
    tstart = time.time()

    if focused:
        debug.show_debug(clock)
        pygame.display.flip()
    timings['screen_display_flip'] = (time.time() - tstart) * 1000

    if opacity < 1:
        opacity += 1/30

    if opacity >= 1:
        opacity = 1

    if needed_update_world:
        print((time.time() - start) * 1000)
        print(timings)
        print("-----------------------")

    return canvas, screen, need_update_world, world, mouse, loaded_chunks, zoom, offset, block_coordinates, paused, screen_blocks, selected_block, picker, blocks, save_data, focused, clock
