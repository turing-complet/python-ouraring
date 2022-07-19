import pandas as pd

from .client import OuraClientV2


def to_pandas(summary, metrics=None, date_key="timestamp"):
    """
    Creates a dataframe from a summary object

    :param summary: A summary object returned from API
    :type summary: list of dictionaries. See https://cloud.ouraring.com/v2/docs#tag/Daily-Activity for example

    :param metrics: The metrics to include in the DF. None includes all metrics
    :type metrics: A list of metric names, or alternatively a string for one metric name

    :param date_key: Column to set as the index
    :type date_key: str
    """

    if isinstance(summary, dict):
        summary = [summary]
    df = pd.DataFrame(summary)
    if df.size == 0:
        return df
    if metrics is not None:
        if type(metrics) == str:
            metrics = [metrics]
        else:
            metrics = metrics.copy()
        # drop any invalid cols the user may have entered
        metrics = [m for m in metrics if m in df.columns]

        # always include summary_date (or date_key, as for bedtime)
        if date_key not in metrics:
            metrics.insert(0, date_key)

        df = df[metrics]
    df[date_key] = pd.to_datetime(df[date_key]).dt.date
    df = df.set_index(date_key)
    return df


class OuraClientDataFrameV2(OuraClientV2):
    """
    Similiar to OuraClientV2, but data is returned instead
    as a pandas.DataFrame object. Each row will correspond to a single day
    of data, indexed by the date.
    """

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        access_token=None,
        refresh_token=None,
        refresh_callback=None,
        personal_access_token=None,
    ):
        super().__init__(
            client_id,
            client_secret,
            access_token,
            refresh_token,
            refresh_callback,
            personal_access_token,
        )

    def activity_df(self, start=None, end=None, metrics=None):
        activity_summary = super().daily_activity(start, end)["data"]
        df = to_pandas(activity_summary, metrics)
        return df

    def heart_rate_df(self, start=None, end=None, metrics=None):
        readiness_summary = super().heartrate(start, end)["data"]
        return to_pandas(readiness_summary, metrics)

    def personal_info_df(self):
        info = super().personal_info()
        return pd.DataFrame(info)

    def sessions_df(self, start=None, end=None, metrics=None):
        sessions = super().session(start, end)["data"]
        return to_pandas(sessions, metrics, date_key="day")

    def tags_df(self, start=None, end=None, metrics=None):
        tags = super().tags(start, end)["data"]
        return to_pandas(tags, metrics)

    def workouts_df(self, start=None, end=None, metrics=None):
        workouts = super().workouts(start, end)["data"]
        return to_pandas(workouts, metrics, date_key="day")

    def sleep_df(self, start=None, end=None, metrics=None):
        raise NotImplementedError

    def readiness_df(self, start=None, end=None, metrics=None):
        raise NotImplementedError
