import numpy as np
import obstacles
import magical_gates


def test_circle_magical_gate():
    circle_magical = magical_gates.GateCircle(4, np.array([1, 2]), np.array(
        [0,0]))
    assert circle_magical.is_location_in_gate(np.array([1, 1]))
    assert circle_magical.get_end_point()[1] == 0
    assert circle_magical.get_end_point()[0] == 0


def test_circle_obstacle():
    circle_obstacle = obstacles.ObstacleCircle(4, [5, 6], 1)
    assert circle_obstacle.is_location_in_obstacle(np.array([4, 4]))
    assert not circle_obstacle.is_location_in_obstacle(np.array([4, 0]))


def test_float_circle_obstacle():
    circle_obstacle = obstacles.ObstacleCircle(4.22, [5.5, 6], 7)
    assert circle_obstacle.is_location_in_obstacle(np.array([8, 4]))
    assert not circle_obstacle.is_location_in_obstacle(np.array([4, 0]))


def test_rectangle_obstacle():
    rectangle_obstacle = obstacles.ObstacleRectangle(4, 5, [5, 6], 4)
    assert not rectangle_obstacle.is_location_in_obstacle(np.array([4, 4]))
    assert rectangle_obstacle.is_location_in_obstacle(np.array([5, 6]))
    assert rectangle_obstacle.is_location_in_obstacle(np.array([7, 7]))
    assert rectangle_obstacle.is_location_in_obstacle(np.array([9, 11]))
    assert not rectangle_obstacle.is_location_in_obstacle(np.array([9, 11.2]))


