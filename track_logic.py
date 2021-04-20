import calculator as calculate
import coordinates
import godot_communicator
import matplotlib.pyplot as plt
import numpy as np
import time

GODOT_IP = '127.0.0.1'
LISTENER_PORT = 4242
UPDATE_INTERVAL = 1 / 60
VELOCITY_MODIFIER = 2.5


def run_simulation(track):
    velocity = 0  # TODO: create car object to store velocity in (among other car-specific values)
    x, y = coordinates.extract_x_and_y_values_lists(track)
    i = 0
    communicator = godot_communicator.Connection(GODOT_IP, LISTENER_PORT)
    while True:
        new_data = communicator.receive_data()
        velocity = get_new_velocity(velocity, is_accelerating(new_data) if new_data else False)
        text = track[i] if not is_derailed(velocity, x, y, i) else 'derailed'
        communicator.send_data(text)
        if velocity != 0:
            # TODO: calculate when to jump to the next coordinate instead of always going on loop
            i = i + 1 if i != len(track) - 1 else 0
            time.sleep(1 / velocity)
        else:
            time.sleep(UPDATE_INTERVAL)  # TODO: investigate absolute 1/60th update time


def get_new_velocity(old_velocity, is_accelerating):
    return calculate.velocity(old_velocity, VELOCITY_MODIFIER if is_accelerating else 0)


def is_accelerating(data):
    return True if b'space' in data else False


def is_derailed(velocity, x, y, i):
    radius = calculate.radius(x[i], x[i - 1], x[i - 2], y[i], y[i - 1], y[i - 2])
    centripetal_force = calculate.centripetal_force(velocity, radius)
    return calculate.is_derailed(centripetal_force)


def plot_track(track):
    colors = np.arange(len(track))
    x, y = coordinates.extract_x_and_y_values_lists(track)
    plt.scatter(x, y, c=colors)
    for i, number in enumerate(colors):
        known_radius = calculate.radius(x[i], x[i-1], x[i-2], y[i], y[i-1], y[i-2])
        fulltext = "Number: {}\nRadius: {}".format(number, round(known_radius))
        plt.annotate(fulltext, (x[i], y[i]), fontsize=7)
        plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    inner_track, outer_track = coordinates.load_tracks()
    run_simulation(outer_track)
