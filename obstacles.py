import numpy as np


class Obstacle:
    """
    This class represents an obstacle.
    """
    def __init__(self):
        self._charge = 0

    def is_location_in_obstacle(self, location: np.ndarray) -> np.bool_:
        raise NotImplementedError("is_location_in_obstacle not implemented")

    def get_charge(self) -> float:
        return self._charge

    def get_location(self) -> np.ndarray:
        raise NotImplementedError("get_location not implemented")


class ObstacleCircle(Obstacle):
    """
    This class represents a circle obstacle.
    """
    def __init__(self, radius: float, center: list[float], charge: float):
        super().__init__()
        if radius > 0:
            self.__radius = radius
        else:
            raise ValueError('radius must be positive')
        self.__center = np.array(center)
        if self.__center.shape != (2,):
            raise ValueError("Invalid shape")
        self._charge = charge

    def is_location_in_obstacle(self, location: np.ndarray) -> np.bool_:
        """
        This method checks if the location is inside the circle obstacle,
         returns True if it is, False otherwise.
        """
        location = np.array(location)
        return np.linalg.norm(self.__center - location) <= self.__radius

    def get_location(self) -> np.ndarray:
        return self.__center


class ObstacleRectangle(Obstacle):
    """
    This class represents a rectangle obstacle.
    """
    def __init__(self, width: float, height: float, start_point: list[int], charge: float):
        super().__init__()
        self.__start_point = np.array(start_point)
        self._charge = charge
        if self.__start_point.shape != (2,):
            raise ValueError("Invalid shape")

        if width > 0 and height > 0:
            self.__end_point = self.__start_point + np.array([width, height])
        else:
            raise ValueError('width and height must be positive')

    def is_location_in_obstacle(self, location: np.ndarray) -> np.bool_:
        location = np.array(location)
        return np.all(np.logical_and(location <= self.__end_point,
                                     location >= self.__start_point))

    def get_location(self) -> np.ndarray:
        return (self.__start_point + self.__end_point) / 2

