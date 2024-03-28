import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class GraphCreator:
    """
    This class is an abstract class for creating graphs.
    """

    def __init__(self):
        self._df = None
        self._path = ""
        self._plot = None
        self._color_palette = None

    def to_csv(self) -> None:
        """
        This method saves the data frame to a csv file.
        """
        self._df.to_csv(self._path + r"\results_csv.csv")

    def to_plot(self) -> None:
        """
        This method saves the plot to a png file.
        """
        sns.set_theme(style="darkgrid")
        self._color_palette = sns.color_palette("Set2", len(self._df['walkers'].unique()))
        self._create_plot()
        self._plot.savefig(self._path + r"\results_graph.png")

    def _create_plot(self) -> None:
        raise NotImplementedError("This method is not implemented")


class StepsDistanceGraph(GraphCreator):
    """
    This class creates a graph of the steps and distance from the origin.
    """

    def __init__(self, path: str, df: pd.DataFrame):
        super().__init__()
        self._df = df
        self._path = path
        self._plot = None

    def _create_plot(self) -> None:
        """
        This method creates the plot.
        """
        self._plot = sns.relplot(data=self._df, x="steps", y="distance",
                                 kind="line", hue='walkers',
                                 palette=self._color_palette,
                                 style='walkers', markers=False, dashes=False)
        self._plot._legend.remove()
        self._plot.fig.suptitle("Distance from Origin", fontsize=18)
        self._plot.set_axis_labels("Steps", "Distance", fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tick_params(axis='both', which='major', labelsize=12)
        x_values = np.linspace(0, self._df['steps'].max(),
                               100)  # Adjust range as needed
        y_values = np.sqrt(x_values)
        plt.plot(x_values, y_values, label='sqrt(x)', color='black',
                 linestyle='-.')
        plt.legend(fontsize='large')
        plt.tight_layout()



class RadiusGraph(GraphCreator):
    """
    This class creates a graph of the radius and steps.
    """

    def __init__(self, path: str, df: pd.DataFrame):
        super().__init__()
        self._df = df
        self._path = path
        self._plot = None

    def _create_plot(self) -> None:
        """
        This method creates the plot.
        """
        self._plot = sns.relplot(
            data=self._df,
            x="radius",
            y="steps",
            kind="line",
            hue='walkers',
            palette=self._color_palette,
            markers=True,
            marker="o",
            dashes=False,
            linewidth=2,
            ci=None
        )

        sns.move_legend(self._plot, "center left", bbox_to_anchor=(0.1, 0.5))

        self._plot.fig.suptitle("Min Steps to Radius", fontsize=16)
        self._plot.set_axis_labels("Radius", "Steps", fontsize=14)

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()


class CrossGraph(GraphCreator):
    """
    This class creates a graph of the cross number and steps.
    """

    def __init__(self, path: str, df: pd.DataFrame):
        super().__init__()
        self._df = df
        self._path = path
        self._plot = None

    def _create_plot(self) -> None:
        """
        This method creates the plot.
        """

        self._plot = sns.histplot(data=self._df, x="steps", y="cross_num",
                                  hue='walkers',
                                  palette=self._color_palette,
                                  multiple="dodge", shrink=.8,
                                  bins=30)
        sns.move_legend(self._plot, "upper left", bbox_to_anchor=(0, 1))
        self._plot.set_title("Cross num of Y axis")
        self._plot = self._plot.figure
        plt.tight_layout()


class DistanceToAxisGraph(GraphCreator):
    """
    This class creates a graph of the distance to the axis and steps.
    """

    def __init__(self, path, df):
        super().__init__()
        self._df = df
        self._path = path
        self._plot = None

        self.__x_df = self._df.drop(columns="distance_to_axis_y")
        self.__y_df = self._df.drop(columns="distance_to_axis_x")

    def _create_plot(self) -> None:
        """
        This method creates the plot.
        """
        plt.figure(figsize=(10, 8))
        plt.subplot(2, 1, 1)
        sns.lineplot(data=self.__x_df, x="steps", y="distance_to_axis_x",
                     hue='walkers', palette=self._color_palette)
        plt.title('Distance to X-axis')

        plt.subplot(2, 1, 2)
        sns.lineplot(data=self.__y_df, x="steps", y="distance_to_axis_y",
                     hue='walkers', palette=self._color_palette)
        plt.title('Distance to Y-axis')

        plt.tight_layout()
        self._plot = plt
