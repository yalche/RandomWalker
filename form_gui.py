import tkinter as tk
import typing
import sim_globals as sg
from ttkbootstrap import Button, Label, Radiobutton, Style
import simulation_gui
from math_helper import *


class BasicForm(tk.Tk):
    """
    This class represents a GUI basic form for the simulation.
    """
    def __init__(self) -> None:
        super().__init__()
        Style(theme='flatly')

        self.title("Gather Info For Simulation")
        self._walkers: list[dict[str, typing.Any]] = []
        self._obstacles: list[dict[str, typing.Any]] = []
        self._magical_gates: list[dict[str, typing.Any]] = []
        self._steps: int = 0
        self._success = Label(self, text="Added!")
        self._error = Label(self, text="Error!")

    def run(self) -> None:
        self.__create_widgets()
        self.mainloop()

    def __create_widgets(self) -> None:
        """
        This method creates the widgets for the form.
        The widgets are buttons for adding walkers, obstacles, magical
        gates, steps_num, flag for route and a button to run the simulation.
        """
        add_walker_button = Button(self,
                                        text="Add Walker",
                                        command=self._add_walker,
                                        style="PRIMARY")
        add_walker_button.grid(row=1, columnspan=2, pady=5)

        add_obstacle_button = Button(self, text="Add Obstacle",
                                 command=self._add_obstacle)
        add_obstacle_button.grid(row=2, columnspan=2, pady=5)

        add_magical_gate_button = Button(self, text="Add MagicalGate",
                                 command=self._add_magical_gate)
        add_magical_gate_button.grid(row=3, columnspan=2, pady=5)

        steps_label = Label(self, text="steps num:", style="PRIMARY")
        steps_label.grid(column=0, row=4, pady=5)

        self.__steps_num = tk.Entry(self, width=10)
        self.__steps_num.grid(column=1, row=4, pady=5)

        self.__show_route()

        run_simulation_button = tk.Button(self, text="Run!",
                                       command=self._run_simulation)
        run_simulation_button.grid(row=6, column=3, pady=5)

    def _call_success(self) -> None:
        """
        This method calls the success label.
        """
        self._success.destroy()
        self._error.destroy()

        self._success = Label(self, text="ADDED !", style="SUCCESS")
        self._success.grid(row=8, columnspan=4)

    def _call_error(self, text="Data Invalid") -> None:
        """
        This method calls the error label.
        """
        self._error.destroy()
        self._success.destroy()

        self._error = Label(self, text=text, style="DANGER")
        self._error.grid(row=8, columnspan=4)

    def __check_data(self) -> None:
        """
        This method check if the data given is valid.
        """
        steps = self.__steps_num.get()
        if steps.isdigit():
            self._steps = int(steps)
            self._call_success()
        else:
            self._call_error()
        if self.__show_route_answer.get() == "show route":
            self._show_route_answer = True
        else:
            self._show_route_answer = False

    def _run_simulation(self) -> None:
        """
        This method runs the simulation.
        """
        self.__check_data()
        if self._walkers and self._steps:
            sim = simulation_gui.SimulationWindow(self._walkers,
                                                  self._obstacles,
                                   self._magical_gates,
                                   self._steps, self._show_route_answer)
            sim.run_sim()
            self.quit()

        elif not self._walkers:
            self._call_error("no walkers added")
        else:
            self._call_error("steps invalid")

    def __show_route(self) -> None:
        """
        This method creates the radio buttons for the flag - showing the route
        """
        options = ["show route", "don't show route"]
        self.__show_route_answer = tk.StringVar(value=options[0])  # Default to
        i = 0
        for option in options:
            radio_button = Radiobutton(self, text=option,
                                               variable=self.__show_route_answer, value=option, style="PRIMARY")
            radio_button.grid(row=5, column=i, pady=5, padx=5)
            i += 1

    def _add_obstacle(self) -> None:
        small_window = ObstacleWindow(self._obstacles)
        small_window.run()

    def _add_magical_gate(self) -> None:
        small_window = MagicalGateWindow(self._magical_gates)
        small_window.run()

    def _add_walker(self) -> None:
        small_window = WalkerWindow(self._walkers)
        small_window.run()


class AddWindow(BasicForm):
    def __init__(self) -> None:
        super().__init__()
        self._values_to_choose: list = []

    def _widgets(self) -> None:
        """
        This method creates the widgets for the Add window.
        """
        self._choose_object_to_add = tk.StringVar(self)
        self._choose_object_to_add.set(self._values_to_choose[0])
        self._choose_object_menu = tk.OptionMenu(self,
                                               self._choose_object_to_add,
                                                 command=self._add_type,
                                      *self._values_to_choose)
        self._choose_object_menu.grid(row=0, column=0)

    def _add_type(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def run(self) -> None:
        """
        This method runs the Add window.
        """
        self._widgets()
        self.mainloop()


class WalkerWindow(AddWindow):
    """
    This class represents a window for adding walkers.
    """
    def __init__(self, walkers: list[dict[str, dict[str, typing.Any]]]):
        super().__init__()
        self.title("Add Walkers")
        self._values_to_choose = list(sg.WALKERS_DICT.keys())
        self._walkers = walkers

    def _add_type(self, *args, **kwargs) -> None:
        """
        This method refers to the relevant func for the given type of walker.
        """
        for child in self.winfo_children():
            if child != self._choose_object_menu:
                child.destroy()

        if args[0] == "WeightedDiscreteWalker2D":
            self.__data_for_weighted_walker()
        elif args[0] == "IonWalker2D":
            self.__data_for_charged_walker()
        else:
            self.__data_for_usual_walker()

    def __data_for_all_walkers(self, command) -> None:
        """
        This method adds the data for all walkers.
        """
        lbl_amount = Label(self, text="num")
        lbl_amount.grid(column=0, row=1)
        self._amount_walkers = tk.Entry(self, width=10)
        self._amount_walkers.grid(column=1, row=1)

        add_walker_button = Button(self, text="add",
                                           command=command,
                                     style="SUCCESS")
        add_walker_button.grid(row=3, column=1)


    def __data_for_weighted_walker(self) -> None:
        self.__data_for_all_walkers(self.__add_weighted_walker)

        lbl_weight = Label(self, text="weight (0 - 1)")
        lbl_weight.grid(column=0, row=2)
        self._amount_weight = tk.Entry(self, width=10)
        self._amount_weight.grid(column=1, row=2)

        directions = list(sg.DIRECTIONS_DICT.keys())
        self._directions_q = tk.StringVar(self)
        self._directions_q.set(directions[0])
        self._options = tk.OptionMenu(self, self._directions_q,
                                      *directions)
        self._options.grid(row=3, column=0)

    def __data_for_usual_walker(self) -> None:
        self.__data_for_all_walkers(self.__add_usual_walker)

    def __data_for_charged_walker(self) -> None:
        self.__data_for_all_walkers(self.__add_charged_walker)

        lbl_charge = Label(self, text="charge")
        lbl_charge.grid(column=0, row=2)
        self.__charge = tk.Entry(self, width=10)
        self.__charge.grid(column=1, row=2)

    def __add_weighted_walker(self) -> None:
        num = self._amount_walkers.get()
        weight = self._amount_weight.get()
        if check_float_positive(weight) and 0 <= float(weight) <= 1 and num.isdigit():
            self._walkers.append({"type": self._choose_object_to_add.get(),
                                  "values": {"num": int(num), "direction":
                    self._directions_q.get(), "weight": float(weight)}})
            self.destroy()
        else:
            self._call_error()

    def __add_usual_walker(self) -> None:
        num = self._amount_walkers.get()
        if num.isdigit():
            self._walkers.append({"type": self._choose_object_to_add.get(),
                                  "values": {"num": int(num)}})
            self.destroy()
        else:
            self._call_error()

    def __add_charged_walker(self) -> None:
        num = self._amount_walkers.get()
        charge = self.__charge.get()
        if num.isdigit() and check_float(charge):
            self._walkers.append({"type": self._choose_object_to_add.get(),
                                  "values": {"num": int(num), "charge": float(charge)}})
            self.destroy()
        else:
            self._call_error()


class ShapesWindow(AddWindow):
    """
    This class represents a window for adding shapes.
    """
    def __init__(self):
        super().__init__()
        self._values_to_choose = list(sg.OBSTACLES_DICT.keys())

    def _add_type(self, *args, **kwargs) -> None:
        """
        This method refers to the relevant type of shape to add.
        """
        for child in self.winfo_children():
            if child != self._choose_object_menu:
                child.destroy()
        if args[0] == "circle":
            self._data_for_circle()
        if args[0] == "rectangle":
            self._data_for_rectangle()

    def _data_for_circle(self) -> None:
        """
        This method adds the data for a circle shape.
        """
        lbl_radius = Label(self, text="radius")
        lbl_radius.grid(column=0, row=1)

        self._amount_radius = tk.Entry(self, width=10)
        self._amount_radius.grid(column=1, row=1)

        lbl_center = Label(self, text="center")
        lbl_center.grid(column=0, row=2)

        lbl_x = Label(self, text="x:")
        lbl_x.grid(column=1, row=2)

        self._x_value = tk.Entry(self, width=10)
        self._x_value.grid(column=2, row=2)

        lbl_y = Label(self, text="y:")
        lbl_y.grid(column=1, row=3)

        self._y_value = tk.Entry(self, width=10)
        self._y_value.grid(column=2, row=3)

        self._add_charge() # for charged obstacles
        self._add_end_point() # for magical gates

        button_add_circle = Button(self, text="add this circle!",
                                         command=self._add_circle, style="SUCCESS")
        button_add_circle.grid(row=7, column=1)

    def _data_for_rectangle(self) -> None:
        """
        This method adds the data for a rectangle shape.
        """
        lbl_width = Label(self, text="width")
        lbl_width.grid(column=0, row=1)
        self._num_width = tk.Entry(self, width=10)
        self._num_width.grid(column=1, row=1)

        lbl_height = Label(self, text="height")
        lbl_height.grid(column=0, row=2)
        self._num_height = tk.Entry(self, width=10)
        self._num_height.grid(column=1, row=2)

        lbl_startpoint = Label(self, text="start point")
        lbl_startpoint.grid(column=0, row=3)

        lbl_x = Label(self, text="x:")
        lbl_x.grid(column=1, row=3)
        self._x_value = tk.Entry(self, width=10)
        self._x_value.grid(column=2, row=3)

        lbl_y = Label(self, text="y:")
        lbl_y.grid(column=1, row=4)
        self._y_value = tk.Entry(self, width=10)
        self._y_value.grid(column=2, row=4)

        self._add_charge()  # for charged obstacles
        self._add_end_point()  # for magical gates

        button_add_circle = Button(self, text="add this rectangle!",
                                         command=self._add_rectangle,
                                         style="SUCCESS")
        button_add_circle.grid(row=8, column=1)

    def _add_end_point(self) -> None:
        return None

    def _add_charge(self) -> None:
        return None

    def _add_rectangle(self) -> None:
        raise NotImplementedError

    def _add_circle(self) -> None:
        raise NotImplementedError


class MagicalGateWindow(ShapesWindow):
    """
    This class represents a window for adding magical gates.
    """
    def __init__(self, magical_gates):
        super().__init__()
        self.title("Add Magical Gates!")
        self._magical_gates = magical_gates

    def _add_end_point(self) -> None:
        """
        This method adds the end point query for the magical gate.
        """
        lbl_end_point = Label(self, text="end point")
        lbl_end_point.grid(column=0, row=5)

        lbl_x_end_point = Label(self, text="x:")
        lbl_x_end_point.grid(column=1, row=5)
        self.__x_value_end_point = tk.Entry(self, width=10)
        self.__x_value_end_point.grid(column=2, row=5)

        lbl_y_end_point = Label(self, text="y:")
        lbl_y_end_point.grid(column=1, row=6)
        self.__y_value_end_point = tk.Entry(self, width=10)
        self.__y_value_end_point.grid(column=2, row=6)

    def _add_circle(self) -> None:
        radius = self._amount_radius.get()
        x = self._x_value.get()
        y = self._y_value.get()
        x_end = self.__x_value_end_point.get()
        y_end = self.__y_value_end_point.get()

        if check_float(x, y, x_end, y_end) and check_float_positive(radius):
            self._magical_gates.append({"type": self._choose_object_to_add.get(),
                                    "radius": float(radius),
                                "center": (float(x), float(y)), "end_point":
                                        (float(x_end), float(y_end))})
            self.destroy()

        else:
            self._call_error()


    def _add_rectangle(self) -> None:
        width = self._num_width.get()
        height = self._num_height.get()
        x = self._x_value.get()
        y = self._y_value.get()
        x_end = self.__x_value_end_point.get()
        y_end = self.__y_value_end_point.get()

        if check_float(x, y, x_end, y_end) and check_float_positive(width,
                                                                    height):
            self._magical_gates.append({"type": self._choose_object_to_add.get(),
                                    "width": float(width),
                                "height": float(height),
                                "start_point": (float(x), float(y)),
                                    "end_point": (float(x_end), float(y_end))})
            self.destroy()
        else:
            self._call_error()


class ObstacleWindow(ShapesWindow):
    def __init__(self, obstacles):
        super().__init__()
        self.title("Add Obstacles")
        self._obstacles = obstacles

    def _add_charge(self):
        lbl_charge = Label(self, text="charge:")
        lbl_charge.grid(column=1, row=6)

        self.__charge = tk.Entry(self, width=10)
        self.__charge.grid(column=2, row=6)

    def _add_circle(self) -> None:
        """
        This method adds a circle obstacle to the obstacles list.
        """
        radius = self._amount_radius.get()
        x = self._x_value.get()
        y = self._y_value.get()
        charge = self.__charge.get()
        if check_float(x, y, charge) and check_float_positive(radius):
            self._obstacles.append({"type": self._choose_object_to_add.get(),
                                    "radius": float(radius), "center": (float(x), float(y)), "charge": float(charge)})
            self.destroy()
        else:
            self._call_error()

    def _add_rectangle(self) -> None:
        """
        This method adds a rectangle obstacle to the obstacles list.
        """
        width = self._num_width.get()
        height = self._num_height.get()
        x = self._x_value.get()
        y = self._y_value.get()
        charge = self.__charge.get()
        if check_float_positive(width, height) and check_float(x, y):
            self._obstacles.append({"type": self._choose_object_to_add.get(),
                                    "width": float(width), "height": float(height), "start_point": (float(x), float(y)),
                                    "charge": float(charge)})
            self.destroy()
        else:
            self._call_error()
