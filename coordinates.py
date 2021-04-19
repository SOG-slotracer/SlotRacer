import json
from pathlib import Path


def load_tracks():
    data = read_from_file()
    return create_tracks(data)


def read_from_file(file_path: Path = Path('data\\track_coordinates.json')):
    with open(file_path, 'r') as file:
        return json.load(file)['track']


def create_tracks(data):
    inner_track = data['inner_track']
    outer_track = data['outer_track']
    return inner_track['part_1'] + inner_track['part_2'] + inner_track['part_3'], \
        outer_track['part_1'] + outer_track['part_2'] + outer_track['part_3']


def extract_x_and_y_values_lists(track):
    x_coord_list = [float(coordinate_set.split(',')[0]) for coordinate_set in track]
    y_coord_list = [float(coordinate_set.split(',')[1]) for coordinate_set in track]
    return x_coord_list, y_coord_list
