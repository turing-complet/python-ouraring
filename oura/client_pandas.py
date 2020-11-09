import pandas as pd

from .client import OuraClient
from .converters import ActivityConverter, SleepConverter, UnitConverter


def to_pandas(summary, metrics=None, date_key="summary_date"):
    """
    Creates a dataframe from a summary object

    :param summary: A summary object returned from API
    :type summary: dictionary of dictionaries. See https://cloud.ouraring.com/docs/readiness for an example

    :param metrics: The metrics to include in the DF. None includes all metrics
    :type metrics: A list of metric names, or alternatively a string for one metric name
    """

    if isinstance(summary, dict):
        summary = [summary]
    df = pd.DataFrame(summary)
    if df.size == 0:
        return df
    if metrics:
        if type(metrics) == str:
            metrics = [metrics]
        else:
            metrics = metrics.copy()
        # drop any invalid cols the user may have entered
        metrics = [m for m in metrics if m in df.columns]

        # summary_date is a required col
        # TODO: handle bedtime
        if "summary_date" not in metrics:
            metrics.insert(0, "summary_date")

        df = df[metrics]
    df[date_key] = pd.to_datetime(df[date_key]).dt.date
    df = df.set_index(date_key)
    return df


class OuraClientDataFrame(OuraClient):
    """
    Similiar to OuraClient, but data is returned instead
    as a pandas.DataFrame object
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

    def sleep_df(self, start=None, end=None, metrics=None, convert=True):
        """
        Create a dataframe from sleep summary dict object.
        The dataframe is minimally edited, i.e 'raw'

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        sleep_summary = super().sleep_summary(start, end)["sleep"]
        df = to_pandas(sleep_summary, metrics)
        if convert:
            return SleepConverter().convert_metrics(df)
        return df

    def activity_df(self, start=None, end=None, metrics=None, convert=True):
        """
        Create a dataframe from activity summary dict object.
        The dataframe is minimally edited, i.e 'raw'

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        activity_summary = super().activity_summary(start, end)["activity"]
        df = to_pandas(activity_summary, metrics)
        if convert:
            return ActivityConverter().convert_metrics(df)
        return df

    def readiness_df(self, start=None, end=None, metrics=None):
        """
        Create a dataframe from ready summary dict object.
        The dataframe is minimally edited, i.e 'raw'

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        readiness_summary = super().readiness_summary(start, end)["readiness"]
        return to_pandas(readiness_summary, metrics)

    def bedtime_df(self, start=None, end=None, metrics=None):
        """
        Create a dataframe from bedtime summary
        The dataframe is minimally edited, i.e 'raw'

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        bedtime_summary = super().bedtime_summary(start, end)["ideal_bedtimes"]
        for s in bedtime_summary:
            s["window_start"] = s["bedtime_window"]["start"]
            s["window_end"] = s["bedtime_window"]["end"]
            del s["bedtime_window"]
        return to_pandas(bedtime_summary, metrics, date_key="date")

    # TODO: use multi index instead of prefix?
    def combined_df_edited(self, start=None, end=None, metrics=None):
        """
        Combines sleep, activity, and summary into one DF
        Some cols are unit converted for easier use or readability.

        If user specifies a metric that appears in all 3 summaries,
        i.e. 'score', then all 3 metrics will be returned.

        Each summary's column is prepended with the summary name.
        i.e. sleep summary 'total' metric will be re-named 'SLEEP.total'

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """

        def prefix_cols(df, prefix):
            d_to_rename = {}
            for col in df.columns:
                if col != "summary_date":
                    d_to_rename[col] = prefix + ":" + col
            return df.rename(columns=d_to_rename)

        sleep_df = self.sleep_df(start, end, metrics)
        sleep_df = prefix_cols(sleep_df, "SLEEP")
        readiness_df = self.readiness_df(start, end, metrics)
        readiness_df = prefix_cols(readiness_df, "READY")
        activity_df = self.activity_df(start, end, metrics)
        activity_df = prefix_cols(activity_df, "ACTIVITY")

        combined_df = sleep_df.merge(readiness_df, on="summary_date").merge(
            activity_df, on="summary_date"
        )
        return combined_df
