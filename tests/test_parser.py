import info_parser


def test_parser() -> None:
    info = info_parser.InfoFromJson(
        r"jsons_for_tests\good_info.json")
    assert info.json_parser()

    info = info_parser.InfoFromJson(
        r"jsons_for_tests\bad_info.json")
    assert not info.json_parser()


def test_parser_walkers() -> None:
    info = info_parser.InfoFromJson(
        r"jsons_for_tests\bad_walker.json")
    assert info.json_parser()
    assert info.check_data_for_simulation()
    walkers, board_1 = info.get_data_for_simulation()
    assert len(walkers) == 5


def test_data_for_stats():
    info = info_parser.InfoFromJson(
        r"jsons_for_tests/info_bad_obstacles.json")
    info.json_parser()
    assert info.check_data_for_simulation() == False

def test_data_for_stats_2():
    info = info_parser.InfoFromJson(
        r"jsons_for_tests/info_bad_stats_data.json")
    info.json_parser()
    assert info.check_data_for_simulation() == True
    assert info.check_data_for_stats() == False