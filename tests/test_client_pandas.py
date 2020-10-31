import json
import os
from datetime import date

import pandas as pd
import pytest

from .mock_client import MockDataFrameClient

client = MockDataFrameClient()


def test_sleep_summary_df():
    """
    Objectives:
    1. Test that dataframe summary_date match the args passed into
    start and end date

    2. Test that the correct number of metrics are being returned

    3. Test raw and edited dataframes are returning correctly named
    fields and correct data types
    """
    start = "2017-11-05"
    end = "2017-11-05"
    df_raw1 = client.sleep_df_raw(start)
    # check all cols are included
    assert df_raw1.shape == (1, 31)
    # check that start date parameter is correct
    assert df_raw1.index[0] == date(2017, 11, 5)

    df_raw2 = client.sleep_df_raw(start, end, metrics=["bedtime_start", "score"])
    # check that correct metrics are being included
    assert df_raw2.shape[1] == 2
    # check that end date parameter is correct
    assert df_raw2.index[-1] == date(2017, 11, 5)
    # check that data type has not been altered
    assert type(df_raw2["bedtime_start"][0]) == str

    # test that  invalid metric 'zzz' is dropped
    df_raw3 = client.sleep_df_raw(start, end, metrics=["bedtime_start", "zzz"])
    assert df_raw3.shape[1] == 1

    # check that bedtime start has been renamed and is now a timestamp
    df_edited = client.sleep_df_edited(start, end, metrics=["bedtime_start", "zzz"])
    assert type(df_edited["bedtime_start_dt_adjusted"][0]) != str


def test_activity_summary_df():
    start = "2016-09-03"
    end = "2016-09-04"
    df_raw1 = client.activity_df_raw(start)
    # check all cols are included
    assert df_raw1.shape == (1, 30)
    assert df_raw1.index[0] == date(2016, 9, 3)

    df_raw2 = client.activity_df_raw(start, end, metrics=["day_start", "medium"])
    assert df_raw2.shape[1] == 2
    assert df_raw2.index[-1] == date(2016, 9, 3)
    assert type(df_raw2["day_start"][0]) == str

    # test that  invalid metric is dropped
    df_raw3 = client.activity_df_raw(start, end, metrics=["day_start", "zzz"])
    assert df_raw3.shape[1] == 1

    # check that day_start has been renamed and is now a timestamp
    df_edited = client.activity_df_edited(start, end, metrics=["day_start", "zzz"])
    assert type(df_edited["day_start_dt_adjusted"][0]) != str


def test_ready_summary_df():
    start = "2016-09-03"
    end = "2016-09-04"
    df_raw1 = client.readiness_df_raw(start)
    # check all cols are included
    assert df_raw1.shape == (1, 11)
    assert df_raw1.index[0] == date(2016, 9, 3)

    df_raw2 = client.readiness_df_raw(
        start,
        end,
        metrics=["score_hrv_balance", "score_recovery_index"],
    )
    assert df_raw2.shape[1] == 2
    assert df_raw2.index[-1] == date(2016, 9, 3)

    # test that  invalid metric is dropped
    df_raw3 = client.readiness_df_raw(start, end, metrics=["score_hrv_balance", "zzz"])
    assert df_raw3.shape[1] == 1

    df_edited = client.readiness_df_edited(start, end, metrics="score_hrv_balance")
    assert pd.DataFrame.equals(df_raw3, df_edited)


@pytest.mark.skip
def test_combined_summary_df():
    combined_df_edited1 = client.combined_df_edited(start="2020-09-30")
    # check all cols are included
    assert combined_df_edited1.shape == (0, 72)
    assert combined_df_edited1.index[0] > date(2020, 9, 29)

    # check start and end dates work accordingly
    combined_df_edited2 = client.combined_df_edited(
        start="2020-09-30",
        end="2020-10-01",
        metrics=["score_hrv_balance", "steps", "efficiency"],
    )
    assert combined_df_edited2.shape[1] == 3
    assert combined_df_edited2.index[-1] < date(2020, 10, 2)

    # test that  invalid metric is dropped
    combined_df_edited2 = client.combined_df_edited(
        start="2020-09-30",
        end="2020-10-01",
        metrics=["score_hrv_balance", "steps", "bedtime_start", "zzz"],
    )
    assert combined_df_edited2.shape[1] == 3

    # check that columns are pre-fixed with their summary name
    assert "ACTIVITY:steps" in combined_df_edited2
    # check that columns are suffixed with unit conversions
    assert "SLEEP:bedtime_start_dt_adjusted" in combined_df_edited2


@pytest.mark.skip
def test_save_xlsx():
    """
    Check that both raw and edited df's save without issue
    """
    df_raw = client.sleep_df_raw(start="2020-09-30")
    df_edited = client.sleep_df_edited(
        start="2020-09-30",
        end="2020-10-01",
        metrics=["bedtime_start", "bedtime_end", "score"],
    )
    raw_file = "df_raw.xlsx"
    edited_file = "df_edited.xlsx"
    client.save_as_xlsx(df_raw, raw_file, sheet_name="hello world")
    client.save_as_xlsx(df_edited, "df_edited.xlsx")
    assert os.path.exists(raw_file)
    assert os.path.exists(edited_file)


@pytest.mark.skip
def test_tableize():
    """
    Check that df was printed to file
    """
    f = "df_tableized.txt"
    df_raw = client.sleep_df_raw(start="2020-09-30", metrics="score")
    client.tableize(df_raw, filename=f)
    assert os.path.exists(f)
