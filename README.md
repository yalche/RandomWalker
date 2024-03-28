# Random_Walker

This project enables the user to simulate a random walker in a 2D grid. The walker can move in four directions: up, down, left, and right. The walker can also move in a diagonal direction. 
Currently, there are five types of random walkers:
1. RandomDirectionWalker2D - The walker moves in a random direction, each 
   step is one unit.
2. RandomDirectionStepWalker2D - The walker moves in a random direction, 
   each step is a random number of units (0.5-1.5).
3. RegularDiscreteWalker2D - The walker moves in a random direction (up, 
   down, left, right), each 
   step is one unit.
4. WeightedDiscreteWalker2D - The walker moves in a random direction (up, 
   down, left, right, origin), each 
   step is one unit. The walker has a higher probability of moving in a 
   certain direction.
5. IonWalker2D - The walker moves in a random direction, the walker has charges 
   and can be attracted or repelled by other charges.

## Running the simulation

You can run the simulation by running the start.py file.
    
```bash
    python start.py -d json_file # for stats
    python start.py -g # for graphical representation
```

## Json_File

The basic structure of the json file is as follows:

```json
{
  "board":
{
  "walkers": [],
  "obstacles": [],
  "magical_gates": []
  },
  "simulation":
  {
    "stop_param": 
    "num_of_simulations":
  },
  "stats":
  {
    "type": 
    "path": 
  }
}
```
Now we will explain each part of the json file:

### Board
This part of the json file contains the information about the board.
The board is a 2D grid where the walkers move. The board has three parts:

1. Walkers - This part contains the information about the walkers. The 
   information about each walker is stored in a dict. Different types of 
   walkers have different attributes:

```bash
walkers = [{"type": "RandomDirectionWalker2D", "values":  {"num": 5}},
{"type": "WeightedDiscreteWalker2D", "values": {"num": 4, "direction": "up","weight": 0.5}},
{"type": "IonWalker2D", "values": {"num": 4, "charge": 1}}]
```
2. Obstacles - This part contains the information about the obstacles. The 
   information about each obstacle is stored in a dict. The obstacle has 
   the following attributes:

```bash
obstacles = [{"type": "circle", "radius": 5, "center": [8, 8], "charge": 1},
{"type": "rectangle", "width": 3, "height": 5, "start_point": [10, 10], "charge": 1}]
```
3. Magical Gates - This part contains the information about the magical gates. 
   The information about each magical gate is stored in a dict. The magical 
   gate has the following attributes:

```bash
magic_gates = [{"type": "circle", "radius":5, "center": [8, 8], "end_point": [0, 0]},
{"type": "rectangle", "width": 3, "height": 5, "start_point": [10, 10], "end_point": [0, 0]}]
```

If the data is invalid, the object will not be added to the board (for 
example, the radius of a CircleObstacle cannot be negative).

### Simulation
This part of the json file contains the information about the 
simulation. The simulation has the following attributes:

1. Stop_param - This attribute contains the information about the stopping 
   parameter. The simulation stops when the stopping parameter is reached. 
   The stopping parameter can be either the number of steps or the radius 
   from the origin to the walker.

2. Num_of_simulations - How many simulations you want to run.

### Stats
This part of the json file contains the information about the 
Stats you want to save. The stats have the following attributes:

1. Type - The type of stats you want to save. The type can be one of the 
   following:
   * DistanceAxisStats: records the distance of the walker from the x, y 
     axes, 
     stop after N steps (given as the stopping parameter). 
   * CrossStats: records the number of times the walker crosses the x, y 
     axes, stop after N steps (given as the stopping parameter).
   * RadiusStats: records the num of steps the walker did in order to reach 
        the radius R from the origin, stop after reaching the radius R (given). 
   * StepsDistanceStats: records the distance of the walker from the origin 
     after each step, stop after N steps (given as the stopping parameter).

2. Path - The path where you want to save the stats. The path should be 
   a directory where you want to save the csv file and the graph.

### example for json_file

```bash
{
  "board":
{
  "walkers": [
    {"type": "RandomDirectionWalker2D", "values":  {"num": 5}},
    {"type": "WeightedDiscreteWalker2D", "values": {"num": 4, "direction": "up","weight": 0.5}},
  {"type": "IonWalker2D", "values": {"num": 4, "charge": 1}}],

  "obstacles": [{"type": "circle", "radius": 5, "center": [8, 8], "charge": 1},
    {"type": "rectangle", "width": 3, "height": 5, "start_point": [10, 10], "charge": 1}],


  "magical_gates": [{"type": "circle", "radius":5, "center": [8, 8], "end_point": [0, 0]},
    {"type": "rectangle", "width": 3, "height": 5, "start_point": [10, 10], "end_point": [0, 0]}]
  },
  "simulation":
  {
    "stop_param": 15,
    "num_of_simulations": 10
  },
  "stats":
  {
    "type": "CrossStats",
    "path": "graphs\\"
  }
}
```

Enjoy!
