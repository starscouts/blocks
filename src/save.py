import os
import zlib
import json

import constants

def save_world(path, chunks):
    checksums = {}
    region_list = []

    if not os.path.exists(path):
        os.mkdir(path)
    else:
        loaded = load_world(path)

        if 'regions' in loaded:
            region_list = loaded['regions']
        if 'checksums' in loaded:
            checksums = loaded['checksums']

    if not os.path.exists(path + "/region"):
        os.mkdir(path + "/region")

    if not os.path.exists(path + "/playerdata"):
        os.mkdir(path + "/playerdata")

    for x in range(len(chunks)):
        for y in range(len(chunks[x])):
            if y is None:
                continue

            print(str(x) + "," + str(y) + ".bcr")

            with open(path + "/region/" + str(x) + "," + str(y) + ".bcr", "wb") as f:
                checksums[str(x) + "," + str(y) + ".bcr"] = hex(zlib.crc32(str.encode(json.dumps(chunks[x][y]))))

                chunk_exists = False

                for region in region_list:
                    if region["file"] == str(x) + "," + str(y) + ".bcr":
                        chunk_exists = True

                if not chunk_exists:
                    region_list.append({
                        "file": str(x) + "," + str(y) + ".bcr",
                        "range": (16 * x, 16 * y, 15 + 16 * x, 15 + 16 * y)
                    })

                f.write(zlib.compress(str.encode(json.dumps(chunks[x][y]))))

    with open(path + "/level.dat", "wb") as f:
        f.write(zlib.compress(str.encode(json.dumps({
            "version": constants.VERSION,
            "checksums": checksums,
            "regions": region_list
        }))))

def load_world(path):
    with open(path + "/level.dat", "rb") as f:
        data = json.loads(zlib.decompress(f.read()))

    print(data)

    regions = data['regions']

    return {
        "version": data['version'],
        "regions": regions
    }

def get_chunk(path, coords):
    if os.path.exists(path + "/region/" + str(coords[0]) + "," + str(coords[1]) + ".bcr"):
        with open(path + "/region/" + str(coords[0]) + "," + str(coords[1]) + ".bcr", "rb") as f:
            data = json.loads(zlib.decompress(f.read()))

            if data is None:
                return [[["bedrock" for _ in range(16)] for _ in range(16)], [["grass_block" for _ in range(16)] for _ in range(16)]]
            else:
                return data
    else:
        return [[["bedrock" for _ in range(16)] for _ in range(16)], [["grass_block" for _ in range(16)] for _ in range(16)]]

def save_chunk(path, file, data):
    checksums = {}
    region_list = []

    if not os.path.exists(path):
        os.mkdir(path)
    else:
        loaded = load_world(path)

        if 'regions' in loaded:
            region_list = loaded['regions']
        if 'checksums' in loaded:
            checksums = loaded['checksums']

    if not os.path.exists(path + "/region"):
        os.mkdir(path + "/region")

    if not os.path.exists(path + "/playerdata"):
        os.mkdir(path + "/playerdata")

    with open(path + "/region/" + file, "wb") as f:
        checksums[file] = hex(zlib.crc32(str.encode(json.dumps(data))))

        chunk_exists = False

        for region in region_list:
            if region["file"] == file:
                chunk_exists = True

        if not chunk_exists:
            region_list.append({
                "file": file,
                "range": (16 * int(file.split(",")[0]), 16 * int(file.split(",")[1].split(".")[0]), 15 + 16 * int(file.split(",")[0]), 15 + 16 * int(file.split(",")[1].split(".")[0]))
            })

        f.write(zlib.compress(str.encode(json.dumps(data))))

    with open(path + "/level.dat", "wb") as f:
        f.write(zlib.compress(str.encode(json.dumps({
            "version": constants.VERSION,
            "checksums": checksums,
            "regions": region_list
        }))))
