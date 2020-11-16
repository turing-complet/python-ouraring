from oura.converters import ActivityConverter, SleepConverter

from .mock_client import MockDataFrameClient


def _check_list_equal(a, b):
    assert sorted(a) == sorted(b)


def test_sleep_default():
    sc = SleepConverter()
    _check_list_equal(SleepConverter.all_metrics, sc.convert_cols)


def test_activity_default():
    ac = ActivityConverter()
    _check_list_equal(ActivityConverter.all_metrics, ac.convert_cols)


def test_user_input():
    expected = ["awake", "deep"]
    sc = SleepConverter(expected)
    _check_list_equal(expected, sc.convert_cols)


def test_warn_invalid_col():
    foo = "foo"
    ac = ActivityConverter([foo])
    assert foo not in ac.convert_cols


def test_hypnogram_helper():
    hypnogram_5min = (
        "443432222211222333321112222222222111133333322221112233333333332232222334"
    )
    sc = SleepConverter()
    result = sc.convert_hypnogram_helper(hypnogram_5min)
    expected = (
        "AARARLLLLLDDLLLRRRRLDDDLLLLLLLLLLDDDDRRRRRRLLLLDDDLLRRRRRRRRRRLLRLLLLRRA"
    )
    assert expected == result


def test_convert_hypnogram():
    client = MockDataFrameClient()
    sleep_df = client.sleep_df(convert_cols=["rem"])
    assert "4" in sleep_df.hypnogram_5min[0]

    sleep_df = client.sleep_df()
    assert "A" in sleep_df.hypnogram_5min[0]
