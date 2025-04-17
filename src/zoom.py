def zoom_in(zoom):
    if zoom[0] > 128:
        zoom = (zoom[0] / 1.5, zoom[1] / 1.5)
    return zoom

def zoom_out(zoom):
    if zoom[0] < 1280:
        zoom = (zoom[0] * 1.5, zoom[1] * 1.5)
    return zoom

def zoom_reset():
    zoom = (1280.0, 720.0)
    offset = (0, 0)
    return zoom, offset

def offset_down(offset):
    offset = (offset[0], offset[1] - 20)
    return offset

def offset_up(offset):
    offset = (offset[0], offset[1] + 20)
    return offset

def offset_right(offset):
    offset = (offset[0] - 20, offset[1])
    return offset

def offset_left(offset):
    offset = (offset[0] + 20, offset[1])
    return offset