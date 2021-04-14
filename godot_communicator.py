import calculator as calculate
import coordinates
import matplotlib.pyplot as plt
import numpy as np
import socket
import threading
import time

velocity = 0


def bind_port(udp_ip, udp_port):
    print("Binding port: %s" % udp_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    print("Binding is complete")
    print("waiting for client")
    data, addr = sock.recvfrom(1024)
    print("received message:", data)
    return sock, addr


def godot_listener(udp_ip, udp_port):
    global velocity
    # listen to if space is pressed (throttled)
    sock, addr = bind_port(udp_ip, udp_port)
    while True:
        try:
            sock.settimeout(0.0001)
            data2, addr2 = sock.recvfrom(1024)
            if b'space' in data2:
                velocity = calculate.velocity(velocity, 5)
        except socket.timeout:
            time.sleep(0.01)
            continue


def godot_sender(udp_ip, udp_port, track):
    global velocity
    x, y = coordinates.extract_x_and_y_values_lists(track)
    sock, addr = bind_port(udp_ip, udp_port)
    i = 0
    while True:
        text = track[i]
        try:
            sock.settimeout(0.0001)
            data2, addr2 = sock.recvfrom(1024)
            sock.sendto(text.encode('utf-8'), addr)
            time.sleep(0.1)
            continue
        except socket.timeout:
            # drive car. sleep amount is inversely dependant of velocity
            velocity = calculate.velocity(velocity, 0)
            radius = calculate.radius(x[i], x[i - 1], x[i - 2], y[i], y[i - 1], y[i - 2])
            centripetal_force = calculate.centripetal_force(velocity, radius)

            print("F: %s" % centripetal_force)

            if calculate.is_derailed(centripetal_force):
                text = "derailed"
            elif velocity == 0:
                time.sleep(0.1)
            else:
                time.sleep(1 / velocity)
                i = i + 1 if i != len(track) - 1 else 0
            sock.sendto(text.encode('utf-8'), addr)
            continue


def plot_track(track):
    colors = np.arange(len(track))
    x, y = coordinates.extract_x_and_y_values_lists(track)
    plt.scatter(x, y, c=colors)
    for i, number in enumerate(colors):
        known_radius = calculate.radius(x[i], x[i-1], x[i-2], y[i], y[i-1], y[i-2])
        fulltext = "Number: {}\nRadius: {}".format(number, round(known_radius)
        plt.annotate(fulltext, (x[i], y[i]), fontsize=7)
    plt.show()


if __name__ == "__main__":
    GODOT_IP = '127.0.0.1'
    track_1, track_2 = coordinates.load_tracks()
    listener = threading.Thread(target=godot_listener, args=(GODOT_IP, 4242))
    sender = threading.Thread(target=godot_sender, args=(GODOT_IP, 2500, track_2))
    listener.start()
    sender.start()
    plot_track(track_2)
