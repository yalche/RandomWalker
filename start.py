import sys
import typing

import pandas as pd

import form_gui
import info_parser
import argparse
import sim_globals
import board
import walker
import tqdm

class Runner:
    def __init__(self):
        self.__run = 0


class GuiRunner(Runner):
    def __init__(self) -> None:
        super().__init__()

    def run_gui(self) -> None:
        """
        This method runs the GUI.
        """
        w = form_gui.BasicForm()
        w.run()


class SimulationRunner(Runner):
    """
    This class runs the simulation.
    """
    def __init__(self, walkers: list[walker.Walker], simulation_board: board.Board,
                 stop_param: int, stats_type: str, path: str):
        super().__init__()
        self.__board = simulation_board
        self.__walkers = walkers

        self.__stop_param = stop_param
        self.__stats_type = stats_type
        self.__path = path
        self._df_list: list[pd.DataFrame] = []
        self.__operations: list[typing.Any] = []
        self._df = pd.DataFrame()

    def __run_simulation(self) -> None:
        """
        This method runs the simulation.
        """
        self.__operations = sim_globals.STATS_DICT[self.__stats_type]
        self._loger = self.__operations[1](self.__stop_param)
        simulator = self.__operations[0](self.__walkers, self.__board,
                                         self.__stop_param)
        simulator.run_simulation(self._loger.get_data)
        self._df_list.append(self._loger.get_df())

    def run_simulations(self, simulations_num: int) -> None:
        for _ in tqdm.trange(simulations_num):
            self.__run_simulation()
        self._df = pd.concat(self._df_list, ignore_index=True)
        self._df = self._loger.aggregate_df(self._df)
        graph = self.__operations[2](self.__path, self._df)
        graph.to_csv()
        graph.to_plot()


def parse_args() -> argparse.Namespace:
    """
    This function parses the arguments from the command line.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-d', nargs='?',
                        help="Path to the json configuration")
    parser.add_argument('-g', action='store_true', help="Generate GUI")
    parser.add_argument('-h','--help', action="help",
                        # default=argparse.SUPPRESS,
                        help=("please read the documentation for more "
                              "information - README.md"))

    args = parser.parse_args()
    return args


def main() -> None:
    args = parse_args()
    if args.g:
        gui_instance = GuiRunner()
        gui_instance.run_gui()

    elif args.d:
        info = info_parser.InfoFromJson(args.d)

        if info.json_parser() and info.check_data_for_simulation() and info.check_data_for_stats():
            walkers, simulation_board = info.get_data_for_simulation()
            operation, path, stop_param, simulations_num = info.get_data_for_stats()
            simulation_instance = SimulationRunner(walkers,
                                                   simulation_board,
                                                   stop_param, operation,
                                                   path)
            simulation_instance.run_simulations(simulations_num)
        else:
            print("**** Invalid Json File. Please check the documentation! "
                  "****")


if __name__ == '__main__':
    main()
