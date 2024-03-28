import walker
import math
import numpy as np
import pytest

ERROR_CONSTANT = 10 ** -15

def test_base_walker() -> None:
    """
    Test the base walker class

    """
    base_walker = walker.Walker()
    try:
        base_walker.walk()
        assert False
    except NotImplementedError:
        assert True


def test_walk_random_direction_walker():
    random_walker = walker.RandomDirectionWalker2D()
    random_walker.optional_step()
    random_walker.walk()
    coordinates = random_walker.get_location()
    radius = math.sqrt(np.sum(coordinates ** 2))
    assert radius - 1 < ERROR_CONSTANT


def test_walk_random_direction_step_walker() -> None:
    random_walker = walker.RandomDirectionStepWalker2D()
    random_walker.optional_step()
    random_walker.walk()
    coordinates = random_walker.get_location()
    radius = math.sqrt(np.sum(coordinates ** 2))
    assert 0.5 <= radius <= 1.5


def test_walk_discrete_walker() -> None:
    discrete_walker = walker.RegularDiscreteWalker2D()
    discrete_walker.optional_step()
    discrete_walker.walk()
    start_location = discrete_walker.get_location()
    discrete_walker.optional_step()
    discrete_walker.walk()
    end_location = discrete_walker.get_location()

    assert (end_location[0] - start_location[0] < ERROR_CONSTANT or
            end_location[1] - end_location[0] < ERROR_CONSTANT)


def test_walk_discrete_walker_with_weight() -> None:
    walker_4 = walker.WeightedDiscreteWalker2D({"direction": "up", "weight":
        0.7})
    for i in range(100):
        walker_4.optional_step()
        walker_4.walk()
    start_location = walker_4.get_location()
    walker_4.optional_step()
    walker_4.walk()
    end_location = walker_4.get_location()
    assert (abs(end_location[0] - start_location[0]) < ERROR_CONSTANT or
            abs(end_location[1] - start_location[1]) < ERROR_CONSTANT
            or start_location[1]/start_location[0] == end_location[1]/end_location[0])
    assert end_location[1] > 0

def test_charged_walker():
    random_walker_pos = walker.IonWalker2D({"charge": 1})
    random_walker_neg = walker.IonWalker2D({"charge": -1})

    list_walkers = [random_walker_pos, random_walker_neg]
    for i in range(10000):
        for walker_ in list_walkers:
            walker_.optional_step(list_walkers, [])
            walker_.walk()
    for walker_ in list_walkers:
        walker_.optional_step(list_walkers, [])
        walker_.walk()
    coordinates_1, coordinates_2 = random_walker_pos.get_location(), random_walker_neg.get_location()
    assert np.linalg.norm(coordinates_1 - coordinates_2) < 2

def test_charged_walker_given_location():
    random_walker_pos = walker.IonWalker2D({"charge": 1})
    random_walker_neg = walker.IonWalker2D({"charge": -1})

    list_walkers = [random_walker_pos, random_walker_neg]
    random_walker_pos.set_next_step(np.array([10, 10]))
    random_walker_neg.set_next_step(np.array([-10, -10]))
    random_walker_neg.walk()
    random_walker_pos.walk()

    start_distance = np.linalg.norm(random_walker_pos.get_location() - random_walker_neg.get_location())
    for i in range(10000):
        for walker_ in list_walkers:
            walker_.optional_step(list_walkers, [])
            walker_.walk()

    coordinates_1, coordinates_2 = random_walker_pos.get_location(), random_walker_neg.get_location()
    assert np.linalg.norm(coordinates_1 - coordinates_2) < start_distance

