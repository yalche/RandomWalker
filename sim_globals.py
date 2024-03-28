import graphs
import walker
import obstacles
import magical_gates
import simulation
import stats
import numpy as np
import typing

MIN_SIM = 1
MAX_SIM = 2 ** 63 - 1

MIN_PARAM = 1
MAX_PARAM = 2 ** 63 - 1

OBSTACLES_DICT = {"circle": obstacles.ObstacleCircle,
                  "rectangle": obstacles.ObstacleRectangle}

MAGICAL_GATES_DICT = {"circle": magical_gates.GateCircle,
                      "rectangle": magical_gates.GateRectangle}

SIMULATION_DICT = {"StepsNumSimulator2D": simulation.StepsNumSimulator2D,
                   "OriginDistanceSimulator2D":
                       simulation.OriginDistanceSimulator2D}

STATS_DICT = {"DistanceAxisStats": [simulation.StepsNumSimulator2D,
                                      stats.DistanceAxisStats, graphs.DistanceToAxisGraph],
              "CrossStats": [simulation.StepsNumSimulator2D,
                             stats.CrossStats, graphs.CrossGraph],
              "RadiusStats": [simulation.OriginDistanceSimulator2D,
                              stats.RadiusStats, graphs.RadiusGraph],
              "DistanceStats": [simulation.StepsNumSimulator2D,
                                      stats.DistanceStats, graphs.StepsDistanceGraph]}


DIRECTIONS_DICT = {"up": np.array([0, 1]), "down": np.array([0, -1]),
                      "left": np.array([-1, 0]),
                      "right": np.array([1, 0]), "origin": np.zeros(2)}

WALKERS_DICT = {"WeightedDiscreteWalker2D": walker.WeightedDiscreteWalker2D,
                "RandomDirectionWalker2D": walker.RandomDirectionWalker2D,
                "RandomDirectionStepWalker2D": walker.RandomDirectionStepWalker2D,
                "RegularDiscreteWalker2D": walker.RegularDiscreteWalker2D,
                "IonWalker2D": walker.IonWalker2D}

