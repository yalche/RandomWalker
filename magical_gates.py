import numpy as np


class MagicalGate:
    """
    This class represents a magical gate.
    """
    def is_location_in_gate(self, location: np.ndarray) -> np.bool_:
        raise NotImplementedError("is_location_in_obstacle not implemented")

    def get_end_point(self) -> np.ndarray:
        raise NotImplementedError("get_end_point not implemented")


class GateCircle(MagicalGate):
    """
    This class represents a circle magical gate.
    """
    def __init__(self, radius: float, center: np.ndarray, end_point: np.ndarray):
        super().__init__()

        if radius > 0:
            self.__radius = radius
        else:
            raise ValueError("radius must be positive")

        self.__center = np.array(center)
        self.__end_point = np.array(end_point)
        if self.__center.shape != (2,) or self.__end_point.shape != (2,):
            raise ValueError("Invalid shape")



    def is_location_in_gate(self, location: np.ndarray) -> np.bool_:
        """
        This method checks if the location is inside the circle magical gate,
         returns True if it is, False otherwise.
        """
        location = np.array(location)
        return np.all(np.linalg.norm(self.__center - location) <=
                      self.__radius)

    def get_end_point(self) -> np.ndarray:
        """
        This method returns the end point of the circle magical gate.
        """
        return self.__end_point


class GateRectangle(MagicalGate):
    """
    This class represents a rectangle magical gate.
    """
    def __init__(self, width: float, height: float, start_point: list[int], end_point: list[int]):
        super().__init__()

        self.__start_point = np.array(start_point)
        self.__end_point = np.array(end_point)
        if self.__start_point.shape != (2,) or self.__end_point.shape != (2,):
            raise ValueError("Invalid shape")

        if width > 0 and height > 0:
            self.__edge_point = self.__start_point + np.array([width, height])
        else:
            raise ValueError("width and height must be positive")

    def is_location_in_gate(self, location: np.ndarray) -> np.bool_:
        """
        This method checks if the location is inside the rectangle magical gate,
         returns True if it is, False otherwise.
        """
        location = np.array(location)
        return np.all(np.logical_and(location <= self.__edge_point,
                                     location >= self.__start_point))

    def get_end_point(self) -> np.ndarray:
        """
        This method returns the end point of the rectangle magical gate.
        """
        return self.__end_point
