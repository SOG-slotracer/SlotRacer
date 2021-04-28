import math
import numpy as np
import sys

CAR_MASS = 1
GRAVITY = 9.81
SLIDING_FRICTION_COEFFICIENT = 0.0001
AIR_FRICTION_COEFFICIENT = 0.00035
DERAIL_THRESHOLD = 5000

SLIDING_FRICTION = CAR_MASS * GRAVITY * SLIDING_FRICTION_COEFFICIENT


def total_force(velocity, throttle_force):
    air_friction = AIR_FRICTION_COEFFICIENT / 2 * pow(velocity, 2)
    return throttle_force - air_friction - SLIDING_FRICTION


def velocity(old_velocity, throttle_force):
    acceleration = total_force(old_velocity, throttle_force) / CAR_MASS
    velocity = acceleration + old_velocity
    return velocity if velocity >= 60 else 0


def radius(x1, x2, x3, y1, y2, y3):
    if x2 - x1 == 0 or x3 - x2 == 0:
        return sys.maxsize
    ma = (y2 - y1) / (x2 - x1)
    mb = (y3 - y2) / (x3 - x2)
    if mb == 0:
        return sys.maxsize
    xc = ((ma * mb * (y1 - y3)) + (mb * (x1 + x2)) - (ma * (x2 + x3))) / (2 * (mb - ma))
    yc = ((-1 / mb) * (xc - ((x2 + x3) / 2))) + ((y2 + y3) / 2)
    radius = math.sqrt((xc - x1) * (xc - x1) + (yc - y1) * (yc - y1))
    return radius


def centripetal_force(velocity, radius):
    return CAR_MASS * pow(velocity, 2) / radius


def is_derailed(centripetal_force):
    return abs(centripetal_force) > DERAIL_THRESHOLD


def new_position(velocity, x1, x2, y1, y2, interval):
    delta_x = x2 - x1
    delta_y = y2 - y1
    total_time_needed = distance(delta_x, delta_y) / velocity
    velocity_x = delta_x / total_time_needed
    velocity_y = delta_y / total_time_needed
    return {'x': x1 + velocity_x * interval,
            'y': y1 + velocity_y * interval,
            'coordinate_reached': coordinate_reached(interval, total_time_needed)}


def distance(delta_x, delta_y):
    distance_pow = pow(delta_x, 2) + pow(delta_y, 2)
    return math.sqrt(abs(distance_pow))


def coordinate_reached(interval, total_time_needed):
    # Due to overshoot on the next loop, a '* 2' is added to go to the next coordinate 1 loop early
    return interval * 2 > total_time_needed
