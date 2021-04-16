import math
import numpy as np
import sys
import time

AIR_FRICTION_COEFFICIENT = 0.07
CAR_MASS = 1
DERAIL_THRESHOLD = 2.5
GRAVITY = 9.81
SLIDING_FRICTION_COEFFICIENT = 0.2
THROTTLE_FORCE = 15

SLIDING_FRICTION = CAR_MASS * GRAVITY * SLIDING_FRICTION_COEFFICIENT


def total_force(velocity, throttle_force):
    air_friction = AIR_FRICTION_COEFFICIENT / 2 * pow(velocity, 2)
    return throttle_force - air_friction - SLIDING_FRICTION


def velocity(old_velocity, previous_timestamp, throttle_force=THROTTLE_FORCE):
    acceleration = total_force(old_velocity, throttle_force) / CAR_MASS
    velocity = old_velocity + acceleration * (time.time() - previous_timestamp)
    return velocity if velocity > 0 else 0


def radius(x1, x2, x3, y1, y2, y3):
    point_1 = np.array([x1, y1])
    point_2 = np.array([x2, y2])
    point_3 = np.array([x3, y3])
    w = math.hypot(x1 - x3, y1 - y3)
    h = np.cross(point_3 - point_1, point_1 - point_2) / np.linalg.norm(point_3 - point_1)
    return pow(w, 2) / (8 * h) + (h / 2) if h != 0 else sys.maxsize


def centripetal_force(velocity, radius):
    return CAR_MASS * pow(velocity, 2) / radius


def is_derailed(centripetal_force):
    return abs(centripetal_force) > DERAIL_THRESHOLD
