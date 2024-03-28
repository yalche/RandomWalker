import random
import math
import typing
import uuid
import numpy as np
import obstacles


class Walker:
    """
    This class represents a walker.
    """

    def __init__(self) -> None:
        """
        Initialize the basic walker.
        Most of the methods are not implemented, Do not use this class directly.
        """
        self._step: float = 0
        self._uuid = str(uuid.uuid4())
        self._charge: float = 0
        self._type = "Walker"

    def get_charge(self) -> float:
        """
        This method returns the charge of the walker.
        """
        return self._charge

    def get_type(self) -> str:
        """
        This method returns the type of the walker.
        """
        return self._type

    def get_uuid(self) -> str:
        """
        This method returns the uuid of the walker.
        """
        return f"{self._type}_{self._uuid}"

    def set_next_step(self, new_next_step: np.ndarray) -> None:
        """
        This method sets the next step of the walker from the outside,
        if needed.
        """
        raise NotImplementedError("This method is not implemented")

    def get_location(self) -> np.ndarray:
        """
        This method returns the current location of the walker.
        """
        raise NotImplementedError("This method is not implemented")

    def _get_direction(self, *args):
        raise NotImplementedError("This method is not implemented")

    def _get_step(self) -> float:
        raise NotImplementedError("This method is not implemented")

    def walk(self) -> None:
        raise NotImplementedError("This method is not implemented")

    def restart(self) -> None:
        raise NotImplementedError("This method is not implemented")

    def optional_step(self, *args) -> np.ndarray:
        raise NotImplementedError("This method is not implemented")


"""
2D Walker classes
"""


class Walker2D(Walker):
    """
    This class represents a walker in 2D.
    There are two types of 2D walkers: ContinuousWalker2D and DiscreteWalker2D.
    Do not use this class directly.
    """
    def __init__(self):
        super().__init__()
        self._location = np.zeros(2)
        self._next_step = np.zeros(2)

    def restart(self) -> None:
        """
        This method resets the walker's location to the origin.
        """
        self._location = np.zeros(2)

    def get_location(self) -> np.ndarray:
        """
        This method returns the current location of the walker.
        """
        return self._location

    def set_next_step(self, new_next_step: np.ndarray) -> None:
        """
        This method sets the next step of the walker from the outside,
        if needed.
        """
        self._next_step = new_next_step


class ContinuousWalker2D(Walker2D):
    """
    This class represents a continuous walker.
    Each time, the walker will move one step in random direction, without
    any restrictions on the direction.
    Do not use this class directly.
    """
    def __init__(self):
        super().__init__()

    def walk(self) -> None:
        """
        This method moves the walker to the next step after validating it.
        """
        self._location = self._next_step

    def optional_step(self, *args) -> np.ndarray:
        """
        This method returns the next step, before validating it.
        """
        direction = self._get_direction(*args)
        step = self._get_step()
        vector = np.array([math.cos(direction), math.sin(direction)]) * step
        self._next_step = self._location + vector
        return self._next_step


class DiscreteWalker2D(Walker2D):
    """
    This class represents a discrete walker.
    Each time, the walker will move one step in random direction,
    from possible given directions.
    Do not use this class directly.
    """
    def __init__(self):
        super().__init__()

    def walk(self) -> None:
        """
        This method moves the walker to the next step after validating it.
        """
        self._location = self._next_step

    def optional_step(self, *args) -> np.ndarray:
        """
        This method returns the next step, before validating it.
        """
        self._next_step = self._location + self._get_direction()
        return self._next_step


class RandomDirectionWalker2D(ContinuousWalker2D):
    """
    This class represents a random walker.
    Each time, the walker will move one step to random direction.
    """
    def __init__(self, *args):
        super().__init__()
        self._step = 1.0
        self._type = "RandomDirectionWalker2D"

    def _get_direction(self, *args) -> float:
        """
        This method returns random direction in radians.
        """
        return random.uniform(0, 2) * math.pi

    def _get_step(self) -> float:
        """
        This method returns the step size.
        """
        return self._step


class RandomDirectionStepWalker2D(ContinuousWalker2D):
    """
    This class represents a random walker.
    Each time, the walker will move random step between [0.5, 1.5]
     in random direction.
    """
    def __init__(self, *args):
        super().__init__()
        self._type = "RandomDirectionStepWalker2D"

    def _get_direction(self, *args) -> float:
        """
        This method returns random direction in radians.
        """
        return random.uniform(0, 2) * math.pi

    def _get_step(self) -> float:
        self.__choose_step()
        return self._step

    def __choose_step(self) -> None:
        """
        This method chooses the step size - between 0.5 and 1.5.
        """
        self._step = random.uniform(0.5, 1.5)


class RegularDiscreteWalker2D(DiscreteWalker2D):
    angles = [np.array([1, 0]), np.array([-1, 0]), np.array([0, -1]),
              np.array([0, 1])]
    """
    This class represents a random walker.
    Each time, the walker will move one step in random direction (up, down, left, right).
    """
    def __init__(self, *args):
        super().__init__()
        self._step: float = 1
        self._type = "RegularDiscreteWalker2D"

    def _get_direction(self, *args) -> np.ndarray:
        return random.choice(RegularDiscreteWalker2D.angles)

    def _get_step(self) -> float:
        return self._step


class WeightedDiscreteWalker2D(DiscreteWalker2D):
    """
    This class represents a random walker.
    Each time, the walker will move random step, in random direction (up,
    down, left, right, toward origin), when the options are weighted
    differently.
    """

    def __init__(self, *args):
        super().__init__()

        self.__angles = {"up": np.array([0, 1]), "down": np.array([0, -1]),
                         "left": np.array([-1, 0]), "right": np.array([1, 0]), "origin": np.zeros(2)}

        self._step: float = 1
        self._next_step = np.zeros(2)

        if args[0]["direction"] in self.__angles.keys():
            self.__direction = args[0]["direction"]
        else:
            raise ValueError("direction must be in " + str(
                self.__angles.keys()))

        if 0 <= args[0]["weight"] <= 1:
            self.__weighted_percent = args[0]["weight"]
        else:
            raise ValueError("weight must be between 0 and 1")

        self._type = f"WeightedDiscreteWalker2D{self.__direction}{self.__weighted_percent}"

    def __get_weights(self) -> list[float]:
        """
        This method returns the weights of the directions.
        """
        usual_percent = (1 - self.__weighted_percent) / (len(self.__angles.keys()) - 1)
        return [self.__weighted_percent if (direction == self.__direction)
                else usual_percent for direction in self.__angles.keys()]

    def __get_direction_toward_origin(self) -> None:
        """
        This method returns the direction toward the origin, based on the current location.
        """
        delta = np.linalg.norm(self._location)
        self.__angles['origin'] = self._location / -delta if delta != 0 else\
            np.zeros(2)

    def _get_direction(self, *args) -> np.ndarray:
        """
        This method returns the direction of the walker.
        """
        self.__get_direction_toward_origin()
        return random.choices(list(self.__angles.values()), self.__get_weights())[0]

    def _get_step(self) -> float:
        return self._step


class IonWalker2D(ContinuousWalker2D):
    """
    This class represents a charged walker.
    """
    def __init__(self, values: dict[str, float]):
        super().__init__()
        self._charge = values["charge"]
        self.__step: float = 2
        self.__uuid = str(uuid.uuid4())
        self._next_step = np.zeros(2)
        self._type = f"IonWalker2DCharge{self._charge}"

    def _get_step(self) -> float:
        return self.__step

    def __get_object_attraction(self, obj: typing.Union[Walker, obstacles.Obstacle])\
            -> np.ndarray:
        """
        This method returns the attraction direction of the walker to another
        object.
        """
        if obj.get_charge() != 0:
            power_vector = self._location - obj.get_location()
            if np.dot(power_vector, power_vector) > 1:
                return (power_vector *
                              ((obj.get_charge() * self._charge) /
                               (np.dot(power_vector, power_vector))))
        return np.zeros(2)

    def _get_direction(self, walkers: list[Walker], obstacles: list[obstacles.Obstacle]) -> np.ndarray:
        """
        This method returns the direction of the walker, based on the
        attraction to other charged walkers and obstacles.
        This method is based on Coulomb's law (F = k * q1 * q2 / r^2).
        """
        direction = np.zeros(2)
        for walker in walkers:
            if walker.get_uuid() != self.__uuid:
                direction += self.__get_object_attraction(walker)
        for obstacle in obstacles:
            direction += self.__get_object_attraction(obstacle)
        return direction

    def optional_step(self, *args) -> np.ndarray:
        """
        This method returns the next step, before validating it.
        The optional step is based on the attraction to other charged
        walkers and obstacles, and a random direction.
        """
        step = self._get_step()
        random_direction = random.uniform(0, 2) * math.pi
        random_direction_array = np.array([math.cos(random_direction),
                                     math.sin(random_direction)])
        direction = self._get_direction(*args)
        self._next_step = self._location + direction * step + random_direction_array
        return self._next_step

