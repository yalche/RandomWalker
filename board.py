import copy
import math
import typing

import obstacles
from obstacles import ObstacleRectangle, ObstacleCircle
import walker
import magical_gates
import numpy as np


class Board:
    """
    This class represents a board, which contains obstacles and magical gates.
    Most of the methods are not implemented, Do not use this class directly.
    """
    def __init__(self):
        self._magical_gates = []
        self._obstacles = []

    def _add_obstacle(self) -> None:
        raise NotImplementedError("add_obstacle is not implemented")

    def get_obstacles(self) -> list[obstacles.Obstacle]:
        return self._obstacles

    def get_magical_gates(self) -> list[magical_gates.MagicalGate]:
        return self._magical_gates

    def move_walkers(self, rand_walkers: list[walker.Walker]) -> None:
        raise NotImplementedError("move_walker is not implemented")


class Board2D(Board):
    """
    This class represents a 2D board, which contains obstacles and magical gates.
    """
    def __init__(self, obstacles: list[dict], magical_gates: list[dict]) -> None:
        super().__init__()
        self._obstacles_dict = obstacles
        self.__add_obstacles()
        self._magical_gates_dict = magical_gates
        self.__add_magical_gates()
        self.__min_size = self.__min_size_board_shapes()

    def __add_obstacles(self) -> None:
        """
        This method adds obstacles to the board, based on the obstacle type.
        """
        obstacles_list = copy.deepcopy(self._obstacles_dict)
        for obstacle_dict in obstacles_list:
            try:
                if obstacle_dict["type"] == "circle":
                    self.__add_circle(obstacle_dict)
                elif obstacle_dict["type"] == "rectangle":
                    self.__add_rectangle(obstacle_dict)
            except ValueError:
                self._obstacles_dict.remove(obstacle_dict)
                print(f"*** Invalid data for {obstacle_dict}, not added ***")

    def __add_circle(self, obstacle_dict: dict[str, typing.Any]) -> \
            None:
        """
        This method adds a circle obstacle to the board.
        """
        new_obstacle = ObstacleCircle(obstacle_dict["radius"],
                                      obstacle_dict["center"],
                                      obstacle_dict["charge"])
        self._obstacles.append(new_obstacle)


    def __add_rectangle(self, obstacle_dict: dict[str, typing.Any]) \
            -> None:
        """
        This method adds a rectangle obstacle to the board.
        """
        new_obstacle = ObstacleRectangle(obstacle_dict["width"],
                                         obstacle_dict["height"],
                                         obstacle_dict["start_point"],
                                         obstacle_dict["charge"])
        self._obstacles.append(new_obstacle)



    def __add_magical_gates(self) -> None:
        """
        This method adds magical gates to the board, based on the gate type.
        """
        magical_gates_list = copy.deepcopy(self._magical_gates_dict)
        for gate_dict in magical_gates_list:
            try:
                if gate_dict["type"] == "circle":
                    self.__add_circle_gate(gate_dict)
                if gate_dict["type"] == "rectangle":
                    self.__add_rectangle_gate(gate_dict)
            except ValueError:
                self._magical_gates_dict.remove(gate_dict)
                print(f"*** Invalid data for {gate_dict}, not added ***")

    def __add_circle_gate(self, gate_dict: dict[str, typing.Any]) -> \
            None:
        """
        This method adds a circle gate to the board.
        """
        new_gate = magical_gates.GateCircle(gate_dict["radius"],
                                      gate_dict["center"],
                                            gate_dict["end_point"])
        self._magical_gates.append(new_gate)

    def __add_rectangle_gate(self, gate_dict: dict[str, typing.Any]) -> None:
        """
        This method adds a rectangle gate to the board.
        """
        new_gate = magical_gates.GateRectangle(gate_dict["width"],
                                         gate_dict["height"],
                                         gate_dict["start_point"],
                                 gate_dict["end_point"])
        self._magical_gates.append(new_gate)


    def __check_if_location_in_obstacle(self, location: np.ndarray) -> (
            bool):
        """
        This method checks if a location is in an obstacle on the board.
        """
        for obstacle in self._obstacles:
            if obstacle.is_location_in_obstacle(location):
                return True
        return False

    def __min_size_board_shapes(self) -> float:
        """
        This method returns the minimum size of the shapes on the board.
        """
        list_sizes = []
        if not self._obstacles_dict + self._magical_gates_dict:
            return math.inf
        for shape in self._obstacles_dict + self._magical_gates_dict:
            if shape["type"] == "rectangle":
                list_sizes.append(min(shape["height"], shape["width"]))
            elif shape["type"] == "circle":
                list_sizes.append(shape["radius"] * 2)
        min_size = min(list_sizes)
        return float(min_size)

    def __check_big_steps(self, random_walker: walker.Walker,
                          optional_location: np.ndarray) -> None:
        """
        This method checks if the vector of optional location is in an
        obstacle or gate,
        and sets the next step accordingly.
        """

        vector = optional_location - random_walker.get_location()
        norm_vector = vector / np.linalg.norm(vector)
        for i in range(1, int(np.linalg.norm(vector))):
            optional_location = random_walker.get_location() + i * norm_vector
            for gate in self._magical_gates:
                if gate.is_location_in_gate(optional_location):
                    random_walker.set_next_step(gate.get_end_point())
                    return
            if self.__check_if_location_in_obstacle(optional_location):
                random_walker.set_next_step(optional_location - norm_vector)
                return
        random_walker.set_next_step(optional_location)

    def __check_next_step(self, random_walker: walker.Walker,
                          optional_location: np.ndarray) -> None:
        """
        This method checks if the next step is in an obstacle or gate,
        and sets the next step accordingly.
        """
        for gate in self._magical_gates:
            if gate.is_location_in_gate(optional_location):
                random_walker.set_next_step(gate.get_end_point())
                return

        if self.__check_if_location_in_obstacle(optional_location):
            optional_location = random_walker.get_location()
            random_walker.set_next_step(optional_location)

    def move_walkers(self, walkers: list[walker.Walker]) -> None:
        """
        This method moves the walkers on the board, by checking if the next
        step is valid, changing it accordingly, and moving the walker.
        """
        for random_walker in walkers:
            optional_location = random_walker.optional_step(walkers,
                                                            self._obstacles)
            if (np.linalg.norm(optional_location -
                               random_walker.get_location())) > self.__min_size:
                self.__check_big_steps(random_walker, optional_location)
            else:
                self.__check_next_step(random_walker, optional_location)
        for random_walker in walkers:
            random_walker.walk()

