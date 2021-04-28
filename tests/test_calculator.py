import pytest
import calculator


def test_total_force():
    velocity = 5
    throttle_force = 7

    # dynamic because original method uses external variables
    air_friction = calculator.AIR_FRICTION_COEFFICIENT / 2 * pow(velocity, 2)
    goal = throttle_force - air_friction - calculator.SLIDING_FRICTION
    assert calculator.total_force(velocity, throttle_force) == goal


@pytest.mark.parametrize('old_velocity, throttle_force, below_treshold', [
    (11, 13, True),
    (125, 325, False)])
def test_velocity(old_velocity, throttle_force, below_treshold):
    if below_treshold:
        goal = 0
    else:
        acceleration = calculator.total_force(old_velocity, throttle_force) / calculator.CAR_MASS
        goal = acceleration + old_velocity
    assert calculator.velocity(old_velocity, throttle_force) == goal


@pytest.mark.parametrize('x1, x2, x3, y1, y2, y3, expected', [
    (3, 4, 3, 3, 4, 5, 1),
    (3, 5, 3, 3, 5, 7, 2),
    (3, 5, 3, 3, 5, 6, 1.5811),
    (0, 1, 3, 0, 2, 4, 7.9057),
    (0, 2, 4, 0, 1, 3, 7.9057)])
def test_radius(x1, x2, x3, y1, y2, y3, expected):
    # expected values retrieved from https://planetcalc.com/8116/
    assert round(calculator.radius(x1, x2, x3, y1, y2, y3), 4) == expected


def test_centripetal_force():
    # value retrieved from https://www.omnicalculator.com/physics/centripetal-force
    # with car mass 1
    assert round(calculator.centripetal_force(17, 19), 2) == 15.21


@pytest.mark.parametrize('centripetal_force', [
    calculator.DERAIL_THRESHOLD + 0.0001,
    -calculator.DERAIL_THRESHOLD - 0.0001])
def test_is_derailed(centripetal_force):
    expected_result = True

    assert calculator.is_derailed(centripetal_force) == expected_result


def test_is_not_derailed():
    centripetal_force = calculator.DERAIL_THRESHOLD
    expected_result = False

    assert calculator.is_derailed(centripetal_force) == expected_result


def test_distance():
    delta_x = 3
    delta_y = 4
    assert calculator.distance(delta_x, delta_y) == 5


def test_new_position():
    velocity = 11
    x1 = 1
    x2 = 4
    y1 = 2
    y2 = 6
    interval = 3
    expected_x = 20.8
    expected_y = 28.4
    expected_coordinate_reached = True

    assert round(calculator.new_position(velocity, x1, x2, y1, y2, interval)['x'], 1) == expected_x
    assert round(calculator.new_position(velocity, x1, x2, y1, y2, interval)['y'], 1) == expected_y
    assert calculator.new_position(velocity, x1, x2, y1, y2, interval)['coordinate_reached'] == \
           expected_coordinate_reached


def test_coordinate_reached():
    interval = 1.1
    total_time_needed = 2
    expected_result = True

    assert calculator.coordinate_reached(interval, total_time_needed) == expected_result


def test_coordinate_not_reached():
    interval = 1
    total_time_needed = 2
    expected_result = False

    assert calculator.coordinate_reached(interval, total_time_needed) == expected_result
