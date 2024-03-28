import json
import os.path
import typing

import sim_globals
import json_scheme
import walker
import board
import jsonschema


class InfoForSimulation:
    """
    Class to parse information for running simulation/stats.
    """
    def __init__(self):
        self._data = None

        self.__walkers = []
        self.__obstacles = []
        self.__magical_gates = []
        self.__board = None

        self.__simulation_param = 0

        self.__path = ""
        self.__operation = None

    def check_data_for_simulation(self) -> bool:
        """
        This method checks if the data for the simulation is valid.
        """
        for r_walker in self._data["board"]["walkers"]:
            if r_walker["type"] not in sim_globals.WALKERS_DICT:
                return False
        for r_obstacle in self._data["board"]["obstacles"]:
            if r_obstacle["type"] not in sim_globals.OBSTACLES_DICT:
                return False
        for r_gate in self._data["board"]["magical_gates"]:
            if r_gate["type"] not in sim_globals.MAGICAL_GATES_DICT:
                return False
        self.__add_walkers()
        if not self.__walkers:
            return False
        return True


    def get_data_for_simulation(self) -> tuple[list[walker.Walker], board.Board]:
        self.__board = board.Board2D(self._data["board"]["obstacles"],
                                     self._data["board"]["magical_gates"])
        return self.__walkers, self.__board

    def __add_walkers(self) -> None:
        for r_walker in self._data["board"]["walkers"]:
            if r_walker["values"]["num"] < 1:
                print(f"**** Invalid Data for {r_walker}, Not added ****")
            for i in range(r_walker["values"]["num"]):
                try:
                    self.__walkers.append(sim_globals.WALKERS_DICT[r_walker["type"]](r_walker["values"]))
                except ValueError:
                    print(f"**** Invalid Data for {r_walker}, Not added ****")

class InfoFromJson(InfoForSimulation):
    """
    Class to parse information from a json file.
    """
    def __init__(self, json_file: str):
        super().__init__()
        self.__json_file = json_file

    def __json_checker(self) -> None:
        """
        This method checks if the json file is in the right format.
        """
        return jsonschema.validate(instance=self._data, schema=json_scheme.data_scheme)

    def json_parser(self) -> bool:
        """
        This method validates the json file and returns True if it is valid.
        """
        # check if there is a json file
        try:
            f = open(self.__json_file)
            self._data = json.load(f)
        except:
            print("**** Couldn't open json file ****")
            return False

        # check if the json id in the right format
        try:
            self.__json_checker()
        except jsonschema.exceptions.ValidationError:
            print("**** The format of the json file is not valid ****")
            return False

        # it is okay to use the data
        return True

    def get_data_for_stats(self) -> tuple[str, str, int, int]:
        """
        This method returns the data for the stats.
        """
        return self.__operation, self.__path, self.__simulation_param, self.__simulation_num

    def check_data_for_stats(self) -> bool:
        """
        This method checks if the data for the stats is valid.
        """
        self.__simulation_param = self._data["simulation"]["stop_param"]
        self.__simulation_num = self._data["simulation"]["num_of_simulations"]
        self.__operation = self._data["stats"]["type"]
        self.__path = self._data["stats"]["path"]
        if not (sim_globals.MIN_SIM <= self.__simulation_num <=
                sim_globals.MAX_SIM):
            return False
        if not (sim_globals.MIN_PARAM <= self.__simulation_param <=
                sim_globals.MAX_PARAM):
            return False
        if self.__operation not in sim_globals.STATS_DICT:
            return False
        if not os.path.isdir(self.__path):
            return False
        return True


class InfoFromGui(InfoForSimulation):
    """
    Class to parse information from the gui.
    """
    def __init__(self, data: dict[str, typing.Any]):
        super().__init__()
        self._data = data


