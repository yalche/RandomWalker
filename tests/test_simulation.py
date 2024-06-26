import simulation_gui


walkers = [
{"type": "IonWalker2D", "values": {"num": 50, "charge": 2}},
{"type": "IonWalker2D", "values": {"num": 50, "charge": -2}}]

magic = [{"type": "circle", "radius": 50, "center":
    [53, 1], "end_point":[-100,-100]}]

obs = [{"type": "circle", "radius": 50,
        "center": [-100,-20],
        "charge": -400
        }]
w = simulation_gui.SimulationWindow(walkers, obs, [], 10000,False)
w.run_sim()

