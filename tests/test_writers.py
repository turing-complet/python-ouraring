import os

from oura.export.writers import save_as_xlsx, tableize

from .mock_client import MockDataFrameClient

client = MockDataFrameClient()


def test_save_xlsx():
    """
    Check that both raw and edited df's save without issue
    """
    df_raw = client.sleep_df(start="2020-09-30", convert=False)
    df_edited = client.sleep_df(
        start="2020-09-30",
        end="2020-10-01",
        metrics=["bedtime_start", "bedtime_end", "score"],
    )
    raw_file = "df_raw.xlsx"
    edited_file = "df_edited.xlsx"
    save_as_xlsx(df_raw, raw_file, sheet_name="hello world")
    save_as_xlsx(df_edited, edited_file)
    assert os.path.exists(raw_file)
    assert os.path.exists(edited_file)


def test_tableize():
    """
    Check df table is correct
    """
    expected = """
+--------------+-------+
| summary_date | score |
+--------------+-------+
|  2017-11-05  |  70   |
+--------------+-------+
    """.strip()
    df = client.sleep_df(start="2020-09-30", metrics="score", convert=False)
    table = tableize(df, is_print=False)
    assert expected == table
