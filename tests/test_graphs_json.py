import info_parser
import graphs
import stats
import simulation

"""
Testing the graphs module - parsing json 
"""

path = r"..\\graphs\\"

def test_graphs_distance_from_axis_json() -> None:
    info = info_parser.InfoFromJson(
        r"jsons_for_tests\good_info.json")
    info.json_parser()
    info.check_data_for_simulation()
    walkers, board = info.get_data_for_simulation()
    loger = stats.DistanceAxisStats(100)
    simulator = simulation.StepsNumSimulator2D(walkers, board, 100)
    simulator.run_simulation(loger.get_data)
    df = loger.get_df()
    graph = graphs.DistanceToAxisGraph(path, df)
    graph.to_csv()
    graph.to_plot()


def test_graphs_radius_json() -> None:
    info = info_parser.InfoFromJson(r"jsons_for_tests\good_info.json")
    info.json_parser()
    info.check_data_for_simulation()
    walkers, board = info.get_data_for_simulation()
    loger = stats.RadiusStats(10)
    simulator = simulation.OriginDistanceSimulator2D(walkers, board, 10)
    simulator.run_simulation(loger.get_data)
    df = loger.get_df()
    graph = graphs.RadiusGraph(path, df)
    graph.to_csv()
    graph.to_plot()


def test_graphs_cross_json() -> None:
    info = info_parser.InfoFromJson(r"jsons_for_tests\good_info.json")
    info.json_parser()
    info.check_data_for_simulation()

    walkers, board = info.get_data_for_simulation()
    loger = stats.CrossStats(10)
    simulator = simulation.StepsNumSimulator2D(walkers, board, 100)
    simulator.run_simulation(loger.get_data)
    df = loger.get_df()
    graph = graphs.CrossGraph(path, df)
    graph.to_csv()
    graph.to_plot()

