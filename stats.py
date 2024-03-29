import numpy as np

import walker
from walker import Walker
import pandas as pd


class Stats:
    """
    This class is responsible for calculating statistics about the simulations.
    """

    def __init__(self):
        self._walkers = []
        self._steps_num = 0
        self._df = pd.DataFrame()
        self._df_aggregated = pd.DataFrame()

    def get_df(self) -> pd.DataFrame:
        """
        This method returns the aggregated data frame.
        """
        self._aggregate_df()
        return self._df_aggregated

    def get_data(self, walkers: list[Walker], steps_num: int) -> None:
        """
        This method gets the data from the simulation.
        This method is called from the simulation class.
        """
        self._walkers = walkers
        self._steps_num = steps_num
        self._calculate_df()

    def _calculate_df(self) -> None:
        raise NotImplementedError("This method is not implemented")

    def _aggregate_df(self) -> None:
        raise NotImplementedError("This method is not implemented")

    def mean(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("This method is not implemented")

class RadiusStats(Stats):
    """
    This class calculates the distance between walkers to the origin,
    and aggregates the data by the radius.
    """
    def __init__(self, *args):
        super().__init__()
        self._df = pd.DataFrame({"walkers": [], "radius": [], "steps": []})
        self._param = args[0]

    def mean(self, df):
        return df.groupby(["walkers", "radius"], as_index=False).mean()

    def _calculate_df(self) -> None:
        """
        This method calculates the distance between walkers to the origin
        and saves the data in the data frame.
        """
        for random_walker in self._walkers:
            distance = np.linalg.norm(random_walker.get_location())
            self._df.loc[len(self._df.index)] = [random_walker.get_uuid(),
                                                 int(distance),
                                                 self._steps_num]

    def _aggregate_df(self) -> None:
        """
        This method aggregates the data frame by the radius.
        """
        self._df.to_csv(r"C:\Users\HP\Desktop\huji\year1\semesterA\CS\EX\new\RandomWalker\graphs\radius.csv")
        self._df = self._df.groupby(["walkers", "radius"],
                                    as_index=False).min()

        self._df["walkers"] = self._df["walkers"].apply(lambda a: a.split("_")[0])
        self._df = self._df[self._df["radius"] <= self._param]
        self._df_aggregated = self._df.groupby(["walkers", "radius"],
                                            as_index=False).mean()


class DistanceAxisStats(Stats):
    """
    This class calculates the distance between walkers to the x and y axes.
    """
    def __init__(self, *args):
        super().__init__()
        self._df = pd.DataFrame({"walkers": [], "steps": [],
                                 "distance_to_axis_x": [],
                                 "distance_to_axis_y": []})

    def mean(self, df):
        return df.groupby(["walkers", "steps"], as_index=False).mean()

    def _aggregate_df(self) -> None:
        """
        This method aggregates the data frame by the number of steps.
        """
        self._df["walkers"] = self._df["walkers"].apply(
            lambda a: a.split("_")[0])
        self._df_aggregated = self._df.groupby(["walkers", "steps"],
                                              as_index=False).mean()

    def _calculate_df(self) -> None:
        """
        This method calculates the distance between walkers to the x and y axes.
        """
        for random_walker in self._walkers:
            distance_x = abs(random_walker.get_location()[1])
            distance_y = abs(random_walker.get_location()[0])
            self._df.loc[len(self._df.index)] = [random_walker.get_uuid(), self._steps_num, distance_x, distance_y]


class DistanceStats(Stats):
    """
    This class calculates the distance between walkers to the origin.

    """
    def __init__(self, *args):
        super().__init__()
        self._df = pd.DataFrame({"walkers": [], "steps": [], "distance": []})

    def mean(self, df):
        return df.groupby(["walkers", "steps"], as_index=False).mean()

    def _aggregate_df(self) -> None:
        """
        This method aggregates the data frame by the number of steps.
        """
        self._df["walkers"] = self._df["walkers"].apply(
            lambda a: a.split("_")[0])
        self._df_aggregated = self._df.groupby(["walkers", "steps"],
                                              as_index=False).mean()

    def _calculate_df(self) -> None:
        """
        This method calculates the distance between walkers to the origin.
        """
        for random_walker in self._walkers:
            distance = np.linalg.norm(random_walker.get_location())
            self._df.loc[len(self._df.index)] = [random_walker.get_uuid(), self._steps_num, distance]


class CrossStats(Stats):
    """
    This class calculates the number of times the walker crossed the y-axis.
    """
    def __init__(self, *args):
        super().__init__()
        self.__previous_step_walkers = {}
        self._draft_df = pd.DataFrame(
            {"walkers": [], "steps": [], "cross_num": []})
        self._df = pd.DataFrame({"walkers": [], "steps": [], "cross_num": []})

    def mean(self, df):
        return df.groupby(["walkers", "steps"], as_index=False).mean()

    def _aggregate_df(self) -> None:
        """
        This method aggregates the data frame by the number of steps.
        """
        self._df["walkers"] = self._df["walkers"].apply(
            lambda a: a.split("_")[0])
        self._df_aggregated = self._df.groupby(["walkers", "steps"],
                                              as_index=False).mean()

    def get_df(self) -> pd.DataFrame:
        """
        This method returns the aggregated data frame.
        """
        self.__arrange_df()
        self._aggregate_df()
        return self._df_aggregated

    def __arrange_df(self) -> None:
        """
        This method arranges the data frame.
        """
        for random_walker in self._walkers:
            for num in range(self._steps_num):
                filtered_df = self._draft_df.loc[
                    (self._draft_df['walkers'] == random_walker.get_uuid())
                    & (self._draft_df["steps"] <= num)]
                cross_sum = filtered_df["cross_num"].sum()
                self._df.loc[len(self._df.index)] = [random_walker.get_uuid(),
                                                     num, cross_sum]

    def _calculate_df(self) -> None:
        """
        This method calculates the number of times the walker crossed the
        y-axis after steps_num steps.
        """
        for random_walker in self._walkers:
            index = self._draft_df.loc[
                (self._draft_df['walkers'] == random_walker.get_uuid())
                & (self._draft_df["steps"] == self._steps_num)].index
            if index.empty:
                self._draft_df.loc[len(self._draft_df.index)] = [random_walker.get_uuid(), self._steps_num, 0]
                index = self._draft_df.loc[(self._draft_df['walkers'] == random_walker.get_uuid())
                                           & (self._draft_df["steps"] == self._steps_num)].index
            if self.__check_if_crossed(random_walker):
                self._draft_df.at[index[0], "cross_num"] += 1
        self.__update_previous_steps_walkers()

    def __check_if_crossed(self, random_walker: walker.Walker) -> bool:
        """
        This method checks if the walker crossed the y-axis.
        """
        if random_walker.get_uuid() in self.__previous_step_walkers.keys():
            prev = self.__previous_step_walkers[random_walker.get_uuid()]
            current = random_walker.get_location()[1]
            if prev < 0 < current or prev > 0 > current:
                return True
        return False

    def __update_previous_steps_walkers(self) -> None:
        """
        This method updates the previous steps of the walkers if needed.
        """
        for random_walker in self._walkers:
            if random_walker.get_location()[1] != 0:
                self.__previous_step_walkers[random_walker.get_uuid()] = (
                    random_walker.get_location())[1]
