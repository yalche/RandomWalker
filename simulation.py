import numpy as np
from walker import Walker
import board
import copy


class Simulator:

    def run_simulation(self, stat_func) -> None:
        raise NotImplementedError("run_simulation is not implemented")

    def _stop_simulation(self) -> bool:
        raise NotImplementedError("stop_simulation is not implemented")


class Simulator2D(Simulator):
    """
    This class represents a simulator for 2D walkers.
    """
    def __init__(self) -> None:
        super().__init__()
        self._walkers: list[Walker] = []
        self._board = board.Board()
        self._steps = 0
        self._num_simulations = 0
        self.__stop = False  # flag to stop simulation

    def stop_simulation(self) -> None:
        self.__stop = True  # change flag to stop simulation

    def continue_simulation(self) -> None:
        self.__stop = False  # change flag to continue simulation

    def run_simulation(self, callback_func) -> None:
        """
        This method runs the simulation while the stop_simulation is False,
        and calls the callback_func at each step (stats or gui).
        """
        self._steps = 0
        while not self._stop_simulation() and not self.__stop:
            callback_func(self._walkers, self._steps)
            self._board.move_walkers(self._walkers)
            self._steps += 1
        callback_func(self._walkers, self._steps)


class StepsNumSimulator2D(Simulator2D):
    """
    This class represents a simulator that stops after a certain number of steps.
    """
    def __init__(self, walkers: list[Walker], simulation_board: board.Board,
                 num_steps: int):
        super().__init__()
        self.__num_steps = num_steps
        self._walkers = copy.deepcopy(walkers)
        self._board = simulation_board

    def _stop_simulation(self):
        """
        This method stops the simulation after a certain number of steps.
        """
        if self._steps == self.__num_steps:
            return True
        return False


class OriginDistanceSimulator2D(Simulator2D):
    """
    This class represents a simulator that stops after a certain distance from the origin.
    """
    def __init__(self, walkers: list[Walker], simulation_board: board.Board,
                 distance: float):
        super().__init__()
        self._walkers = walkers
        self._board = simulation_board
        self.__distance = distance
        self.__relevant_walkers: list[str] = []
        self.__init_walkers()

    def __init_walkers(self):
        """
        This method initializes the valid walkers for the simulation.
        """
        for walker in self._walkers:
            self.__relevant_walkers.append(walker.get_uuid())

    def _stop_simulation(self):
        """
        This method stops the simulation after a certain distance from the origin.
        """
        for walker in self._walkers:
            if walker.get_uuid() in self.__relevant_walkers:
                if np.linalg.norm(walker.get_location()) < self.__distance:
                    return False
                else:
                    self.__relevant_walkers.remove(walker.get_uuid())
        return True
