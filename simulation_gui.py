import tkinter as tk
import pandas as pd

import board
import simulation
import walker
from walker import Walker
import random
import info_parser
from ttkbootstrap import Button, Label, Style
import threading
import numpy as np


class SimulationWindow(tk.Tk):
    """
    This class is responsible for the simulation window GUI.
    """
    def __init__(self, walkers: list[dict], obstacles: (
        list)[dict],
                 magical_gates: list[dict],
                 num_steps: int, route_flag=False):
        super().__init__()

        # data from caller function
        self._walkers_list = walkers
        self._obstacles = obstacles
        self._magical_gates = magical_gates
        self.__route_flag = route_flag

        # data for simulation
        self._board = board.Board()
        self._walkers: list[walker.Walker] = []
        self._num_steps = num_steps
        self.__walkers_points: dict[str, int] = {}
        self.sim_thread = None

        # data for window configure
        self._colors: dict[str, str] = {}
        self.title("Simulation Window")
        self.geometry("1100x700")
        self._canvas = tk.Canvas(self, width=800, height=600)
        self._canvas.grid(rowspan=50, columnspan=3)
        self._canvas_middle = [int(self._canvas['width']) / 2,
                               int(self._canvas['height']) / 2]
        self.__radius_length = 4

        # data for stats
        self._step_counter = 0
        self.__distance_sum = 0

    def __widgets(self) -> None:
        """
        This method creates all widgets for the simulation window.
        """
        exit_button = Button(self, text='Exit', width=25,
                             command=self._exit, style="PRIMARY")
        exit_button.grid(row=51, column=0)

        self.__start_button = Button(self, text='Start', width=25,
                                     command=self.__run_simulation, style="SUCCESS")
        self.__start_button.grid(row=51, column=2)

        restart_button = Button(self, text='restart', width=25,
                                command=self.__restart_simulation,
                                style="SECONDARY")
        restart_button.grid(row=51, column=1)

        self.__stats_chart()
        self.__create_axis()
        self.__draw_shapes(self._obstacles, "#e76f51", "Obstacle")
        self.__draw_shapes(self._magical_gates, "#2a9d8f", "Magic Gate")
        self.__parse_data()
        self.__create_walkers_points()
        self.__walkers_chart()

    def _exit(self) -> None:
        self._simulator.stop_simulation()
        self.destroy()

    def __create_walkers_points(self) -> None:
        """
        This method creates the walkers points on the canvas.
        """
        self.__define_colors()
        radius = self.__radius_length
        for r_walker in self._walkers:
            name = r_walker.get_uuid()
            walker_type = r_walker.get_type()
            self.__walkers_points[name] = self._canvas.create_oval(
                self._canvas_middle[0] - radius, self._canvas_middle[1] - radius,
                self._canvas_middle[0] + radius,
                self._canvas_middle[1] + radius, fill=self._colors[walker_type])
            self._canvas.grid()

    def __to_canvas_coordinates(self, coords: list[float]) -> np.ndarray:
        """
        This method converts the coordinates to the canvas coordinates.
        """
        canvas_middle = np.array([int(self._canvas['width']) / 2, int(self._canvas['height']) / 2])
        canvas_direction = np.array([1, -1])
        new_coords = np.array(coords) * canvas_direction + canvas_middle
        return new_coords

    def __draw_shapes(self, list_shapes, color, shape_type):
        for shape in list_shapes:
            if shape["type"] == "circle":
                center = self.__to_canvas_coordinates(shape["center"])
                self.__draw_circle(center[0], center[1], shape["radius"], color)
                charge = 0
                if "charge" in shape.keys():
                    charge = str(shape["charge"])
                self._canvas.create_text(float(center[0]), float(center[1]),
                                         text=shape_type + "charge" + charge,
                                         activefill="red", fill="black")
            elif shape["type"] == "rectangle":
                self.__draw_rectangle(shape, color, shape_type)

    def __draw_rectangle(self, shape, color, shape_type) -> None:
        """
        This method draws a rectangle on the canvas.
        """
        start_point = self.__to_canvas_coordinates(shape["start_point"])
        x_start = start_point[0] + self.__radius_length
        x_end = start_point[0] + shape["width"]
        y_start = start_point[1] - shape["height"] + self.__radius_length
        y_end = start_point[1]
        self._canvas.create_rectangle(float(x_start), y_start, float(x_end), float(y_end), fill=color)
        self._canvas.create_text((x_start + x_end)/2, (y_start + y_end)/2,
                                 text=shape_type + "charge" + str(shape["charge"]),
                                 activefill="white", fill="black")
        self._canvas.grid()

    def __draw_circle(self, x, y, radius, color) -> None:
        """
        This method draws a circle on the canvas, according to the center point,
        radius and color.
        """
        self._canvas.create_oval(x - radius + self.__radius_length,
                                 y - radius + self.__radius_length,
                                 x + radius, y + radius, fill=color)
        self._canvas.grid()

    def __move_points(self) -> None:
        """
        This method moves the points, painting the points without their route.
        """
        for r_walker in self._walkers:
            name = r_walker.get_uuid()
            point = r_walker.get_location()
            x_next, y_next = self.__calculate_next_location(point)
            self._canvas.moveto(self.__walkers_points[name], x_next, y_next)
        self.__update_stats()
        self._canvas.grid()

    def __calculate_next_location(self, point: np.ndarray) -> tuple[float, float]:
        """
        This method calculates the next location of the walker,
        according to the point, canvas middle and radius length.
        """
        x_next = self._canvas_middle[0] + point[0] - self.__radius_length
        y_next = self._canvas_middle[1] - point[1] - self.__radius_length
        return float(x_next), float(y_next)

    def __move_points_with_route(self) -> None:
        """
        This method moves the points, painting the points and their route.
        """
        for r_walker in self._walkers:
            name = r_walker.get_uuid()
            point = r_walker.get_location()
            walker_type = r_walker.get_type()

            x_next, y_next = self.__calculate_next_location(point)
            location = self._canvas.coords(self.__walkers_points[name])
            x_current = location[0] + self.__radius_length
            y_current = location[1] + self.__radius_length

            self._canvas.create_line(x_current, y_current,
                                                         x_next, y_next,
                                                         fill=self._colors[walker_type],
                                                         width=0.01,
                                                         tags="line_tag")
            self._canvas.moveto(self.__walkers_points[name], x_next, y_next)
            self._canvas.tag_raise(self.__walkers_points[name])
        self.__update_stats()
        self._canvas.grid()

    def __stats_chart(self) -> None:
        """
        This method creates the steps chart.
        """
        self.__step_counter_label = tk.Label(self, text=f"Step:"
                                                      f" {self._step_counter}",
                                          width=25, bg="black", fg="white")
        self.__step_counter_label.grid(row=0, column=4)

    def __create_axis(self) -> None:
        """
        This method creates the axis for the canvas.
        """
        self._canvas.create_line(self._canvas_middle[0], 0,
                                 self._canvas_middle[0], self._canvas["height"],
                                 fill="black", width=1)
        self._canvas.create_line(0, self._canvas_middle[1], self._canvas["width"],
                                 self._canvas_middle[1],
                                 fill="black", width=1)

    def __walkers_chart(self) -> None:
        """
        This method creates the walkers chart, with their colors and their
        stats.
        """
        i = 1
        self.__distances_stats = {}
        self.__distances_axis_stats = {}
        for walker in self._colors.keys():
            color_label = tk.Label(self, text=walker, width=25)
            color_label.config(bg=self._colors[walker], fg="white")
            color_label.grid(row=i, column=4)

            self.__distances_stats[walker] = Label(self, text=f"Distance "
                                                              f"from Origin: 0")
            self.__distances_stats[walker].grid(row=i + 1, column=4)
            self.__distances_axis_stats[walker] = [Label(self,
                                                        text=f"Distance from Y axis: 0"), Label(self,
                                                                                               text=f"Distance from X axis: 0")]
            self.__distances_axis_stats[walker][0].grid(row=i + 2, column=4)
            self.__distances_axis_stats[walker][1].grid(row=i + 3, column=4)
            i += 4

    def __stop_simulation(self) -> None:
        """
        This method stops the simulation.
        """
        self._simulator.stop_simulation()
        self.__start_button.destroy()
        self.__start_button = Button(self, text='Continue', width=25,
                                     command=self.__run_simulation,
                                     style="SUCCESS")
        self.__start_button.grid(row=51, column=2)

    def __run_simulation(self) -> None:
        """
        This method runs the simulation.
        """
        self.sim_thread = threading.Thread(target=self.__simulation_thread)
        self.sim_thread.start()
        self.__start_button = Button(self, text='Stop', width=25,
                                     command=self.__stop_simulation,
                                     style="DANGER")
        self.__start_button.grid(row=51, column=2)

    def __restart_simulation(self) -> None:
        """
        This method restarts the simulation by restarting the walkers,
        and deleting the lines drawn.
        """
        self._step_counter = 0
        self.__step_counter_label.config(text=f"Step: {self._step_counter}")
        for walker in self._walkers:
            walker.restart()
        self.__move_points()
        self._canvas.delete("line_tag")


    def __simulation_thread(self) -> None:
        """
        This method runs the simulation in a thread.
        """
        try:
            self._simulator = simulation.StepsNumSimulator2D(self._walkers,
                                                       self._board,
                                                       self._num_steps)
            self._simulator.run_simulation(self.get_data)
            self.__start_button = Button(self, text='Continue', width=25,
                                         command=self.__run_simulation,
                                         style="SUCCESS")
            self.__start_button.grid(row=51, column=2)
        except tk.TclError:
            print("*** thread closed after destroy ***")

    def __parse_data(self) -> None:
        """
        This method parses the data from the GUI.
        """
        data = {"board": {"walkers": self._walkers_list, "obstacles":
            self._obstacles, "magical_gates": self._magical_gates}, "simulation": {
            "num_of"}}
        parser = info_parser.InfoFromGui(data)
        parser.check_data_for_simulation()
        self._walkers, self._board = parser.get_data_for_simulation()

    def run_sim(self) -> None:
        """
        This method builds and runs the simulation window.
        """
        Style(theme='flatly')
        self.__widgets()
        self.mainloop()

    def get_data(self, walkers: list[Walker], steps_num: int) -> None:
        """
        This method gets the data from the simulation.
        This method is called from the simulation class.
        """
        self._walkers = walkers
        self._step_counter += 1
        self.__step_counter_label.config(text=f"Step: {self._step_counter}",
                                         bg="black", fg="white")
        if self.__route_flag:
            self.__move_points_with_route()
        else:
            self.__move_points()

    def __update_stats(self) -> None:
        """
        This method updates the stats of the walkers.
        """
        self.__update_stats_df()
        df = self._df
        for walker in self.__distances_stats.keys():
            self.__distances_stats[walker].config(
                text=f"Distance to Origin: "
                     f"{df.loc[df['walkers'] == walker]['distance'].iloc[0]:.2f}")
            self.__distances_axis_stats[walker][0].config(
                text=f"Distance to Y axis: "
                     f"{df.loc[df['walkers'] == walker]['distance_y'].iloc[0]:.2f}")
            self.__distances_axis_stats[walker][1].config(
                text=f"Distance to X axis: "
                     f"{df.loc[df['walkers'] == walker]['distance_x'].iloc[0]:.2f}")

    def __update_stats_df(self) -> None:
        """
        This method updates the stats data frame.
        """
        self._df = pd.DataFrame({"walkers": [], "distance": [],
                                 "distance_x": [], "distance_y": []})
        for random_walker in self._walkers:
            distance = np.linalg.norm(random_walker.get_location())
            distance_x = abs(random_walker.get_location()[1])
            distance_y = abs(random_walker.get_location()[0])
            self._df.loc[len(self._df.index)] = [random_walker.get_uuid(),
                                                 distance, distance_x, distance_y]
        self._df["walkers"] = self._df["walkers"].apply(lambda a: a.split("_")[0])
        self._df = self._df.groupby(["walkers"], as_index=False).mean()

    def __define_colors(self) -> None:
        """
        This method defines the colors for the walkers, choosing randomly.
        """
        for walker in self._walkers:
            self._colors[walker.get_type()] = "#"+''.join(
                random.choices('0123456789ABCDEF', k=6))

