import os

import pytest

from .mock_client import MockDataFrameClient

client = MockDataFrameClient()


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
