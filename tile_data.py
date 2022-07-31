from json import load

with open("json_data/tile_info.json") as json_file:
    TILE_DATA = load(json_file)
