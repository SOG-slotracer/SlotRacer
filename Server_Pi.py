import matplotlib.pyplot as plt
import math
import numpy as np
import socket
import time
import threading

UDP_IP = ' 127.0.0.1'
# UDP_PORT = 4242

inner_track_p1 = [
    "376.332703,327.166351", "327.332703,327.166351", "283.332703,322.166351",
    "231.332703,329.166351", "183.332703,324.166351", "139.332703,319.166351",
    "105.332703,303.166351", "85.332703,270.166351", "73.332703,231.166351",
    "71.332703,191.166351", "78.332703,146.166351", "87.332703,121.166351",
    "106.332703,94.166351", "139.332703,72.166351", "172.332703,76.166351",
    "196.332703,96.166351", "216.332703,125.166351", "227.332703,157.166351",
    "244.332703,182.166351", "260.332703,196.166351", "274.332703,211.166351",
    "309.332703,223.166351", "348.332703,224.166351", "400.332703,222.166351",
    "431.332703,223.166351"]
inner_track_p2 = ["475.332703,222.166351", "519.332703,225.166351",
                  "549.332703,219.166351", "596.332703,221.166351"]
inner_track_p3 = [
    "647.332703,224.166351", "684.332703,224.166351", "719.332703,237.166351",
    "745.332703,260.166351", "756.332703,289.166351", "763.332703,318.166351",
    "769.332703,348.166351", "763.332703,379.166351", "751.332703,420.166351",
    "723.332703,461.166351", "693.332703,474.166351", "651.332703,463.166351",
    "624.332703,430.166351", "607.332703,391.166351", "586.332703,357.166351",
    "550.332703,331.166351", "499.332703,324.166351", "458.332703,323.166351",
    "411.332703,324.166351"]

outer_track_p1 = [
    "396.332703,374.166351", "354.332703,373.166351", "309.332703,371.166351",
    "276.332703,372.166351", "227.332703,372.166351", "173.332703,372.166351",
    "123.332703,365.166351", "86.332703,337.166351", "66.332703,310.166351",
    "50.332703,272.166351", "40.332703,230.166351", "42.332703,188.166351",
    "45.332703,154.166351", "53.332703,118.166351", "66.332703,82.166351",
    "94.332703,49.166351", "121.332703,32.166351", "167.332703,27.166351",
    "197.332703,43.166351", "226.332703,70.166351", "243.332703,103.166351",
    "259.332703,137.166351", "275.332703,156.166351", "309.332703,173.166351",
    "353.332703,173.166351", "403.332703,175.166351", "433.332703,175.166351"]
outer_track_p2 = ["469.332703,171.166351", "510.332703,172.166351",
                  "546.332703,170.166351", "590.332703,170.166351"]
outer_track_p3 = [
    "639.332703,173.166351", "673.332703,171.166351", "711.332703,180.166351",
    "742.332703,201.166351", "764.332703,229.166351", "780.332703,256.166351",
    "787.332703,284.166351", "795.332703,312.166351", "797.332703,359.166351",
    "793.332703,398.166351", "780.332703,431.166351", "772.332703,457.166351",
    "756.332703,484.166351", "731.332703,508.166351", "699.332703,523.166382",
    "658.332703,518.166382", "626.332703,495.166351", "603.332703,463.166351",
    "581.332703,423.166351", "556.332703,385.166351", "514.332703,375.166351",
    "471.332703,373.166351", "430.332703,374.166351"]

inner_to_outer_track = ["470.332703,213.166351", "518.332703,205.166351",
                        "561.332703,190.166351", "612.332703,181.166351"]
outer_to_inner_track = ["459.332703,179.166351", "496.332703,186.166351",
                        "531.332703,197.166351", "568.332703,203.166351",
                        "608.332703,215.166351"]

final_track = inner_track_p1 + inner_track_p2 + inner_track_p3 + inner_track_p1 + \
    inner_to_outer_track + outer_track_p3 + outer_track_p1 + \
    outer_to_inner_track + inner_track_p3
final_track2 = outer_track_p1 + outer_to_inner_track + inner_track_p3 + \
    inner_track_p1 + inner_track_p2 + inner_track_p3 + \
    inner_track_p1 + inner_to_outer_track + outer_track_p3

velocity = 0
mass = 1


def port_watcher(port):
    # listen to if space is pressed (throttled)

    UDP_IP = "127.0.0.1"
    UDP_PORT = port

    print("Binding port: %s" % port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("Binding is complete")
    print("waiting for client")
    data, addr = sock.recvfrom(1024)
    print("received message:", data)
    while True:
        # text = final_track[i]
        try:
            sock.settimeout(0.0001)
            data2, addr2 = sock.recvfrom(1024)
            # print(data2)
            if b'space' in data2:
                # space is found over the first port watcher
                # increase speed

                # print("increase force!!")
                calc_velocity(5)
            # sock.sendto(text.encode('utf-8'), addr)
        except socket.timeout:
            time.sleep(0.01)
            # sock.sendto(text.encode('utf-8'), addr)
            continue


def port_watcher2(port):

    UDP_IP = "127.0.0.1"
    UDP_PORT = port

    print("Binding port: %s" % port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("Binding is complete")
    print("waiting for client")
    i = 0
    data, addr = sock.recvfrom(1024)
    print("received message:", data)
    while True:
        text = final_track2[i]
        try:
            sock.settimeout(0.0001)
            data2, addr2 = sock.recvfrom(1024)
            # print("data2: %s" % data2)
            sock.sendto(text.encode('utf-8'), addr)
            time.sleep(0.1)

            continue
        except socket.timeout:
            # drive car. sleep amount is inversely dependant of velocity
            calc_velocity(0)

            # calculate centripetal force
            x = convert_coordinates(final_track2)[0]
            y = convert_coordinates(final_track2)[1]
            radius = calc_radius(x[i], x[i - 1], x[i - 2], y[i], y[i - 1], y[i - 2])
            centripetal_force = mass * velocity * velocity / radius
            print("F: %s" % centripetal_force)

            if velocity == 0:
                time.sleep(0.1)
                # print("stopped")
            else:
                # print("driving")
                time.sleep(1 / velocity)
                i += 1
                if i == len(final_track2):
                    i = 0

            # print("text2: %s" % text)
            sock.sendto(text.encode('utf-8'), addr)

            continue


x = threading.Thread(target=port_watcher, args=(4242,))
x2 = threading.Thread(target=port_watcher2, args=(2500,))

x.start()
x2.start()


def calc_velocity(throttle_force):
    global velocity

    sliding_friction = mass * 9.8 * 0.1
    air_friction = 0.005 * 0.5 * velocity * velocity
    total_force = throttle_force - air_friction - sliding_friction
    acceleration = total_force / mass

    velocity = acceleration + velocity
    if velocity < 2:
        velocity = 0
    # print("v: %s" % velocity)


def convert_coordinates(track_part):
    x = [float(item.split(",")[0]) for item in track_part]
    y = [float(item.split(",")[1]) for item in track_part]
    return x, y


def calc_radius(x1, x2, x3, y1, y2, y3):
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    p3 = np.array([x3, y3])
    w = math.hypot(x1 - x3, y1 - y3)
    h = np.cross(p3 - p1, p1 - p2) / np.linalg.norm(p3 - p1)
    if h != 0:
        radius = pow(w, 2)/(8*h) + (h/2)
    else:
        # If a line is completely flat, set curvature extremely high manually. avoid division by 0
        radius = 99999
    return radius


print(convert_coordinates(final_track2)[0])
print(convert_coordinates(final_track2)[1])

track_parts = [inner_track_p1, inner_track_p2, inner_track_p3, outer_track_p1,
               outer_track_p2, outer_track_p3, inner_to_outer_track, outer_to_inner_track]

colors = np.arange(len(final_track2))
plt.scatter(convert_coordinates(final_track2)[0], convert_coordinates(final_track2)[1], c=colors)
x = convert_coordinates(final_track2)[0]
y = convert_coordinates(final_track2)[1]
for i, number in enumerate(colors):

    fulltext = "Number: {}".format(number)

    known_radius = calc_radius(x[i], x[i-1], x[i-2], y[i], y[i-1], y[i-2])
    fulltext = "Number: {}\nRadius: {}".format(number, known_radius)
    plt.annotate(fulltext, (convert_coordinates(final_track2)[
                 0][i], convert_coordinates(final_track2)[1][i]), fontsize=7)

plt.show()
