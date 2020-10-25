import pandas as pd

from .client import OuraClient


class OuraClientDataFrame(OuraClient):
    """
    Similiar to OuraClient, but data is returned instead
    as a pandas.DataFrame (df) object
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

    def __summary_df(self, summary, metrics=None):
        """
        Creates a dataframe from a summary object

        :param summary: A summary object returned from API
        :type summary: dictionary of dictionaries. See https://cloud.ouraring.com/docs/readiness for an example

        :param metrics: The metrics to include in the DF. None includes all metrics
        :type metrics: A list of metric names, or alternatively a string for one metric name
        """
        df = pd.DataFrame(summary)
        if metrics:
            if type(metrics) == str:
                metrics = [metrics]
            else:
                metrics = metrics.copy()
            # drop any invalid cols the user may have entered
            metrics = [metric for metric in metrics if metric in df.columns]
            # summary_date is a required col
            if "summary_date" not in metrics:
                metrics.insert(0, "summary_date")
            df = df[metrics]
        df["summary_date"] = pd.to_datetime(df["summary_date"]).dt.date
        df = df.set_index("summary_date")
        return df

    def sleep_df_raw(self, start=None, end=None, metrics=None):
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
        sleep_summary = self.sleep_summary(start, end)["sleep"]
        return self.__summary_df(sleep_summary, metrics)

    def sleep_df_edited(self, start=None, end=None, metrics=None):
        """
        Create a dataframe from sleep summary dict object.
        Some cols are unit converted for easier use or readability.

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        sleep_df = self.sleep_df_raw(start, end, metrics)
        sleep_df = SleepConverter().convert_metrics(sleep_df)
        return sleep_df

    def activity_df_raw(self, start=None, end=None, metrics=None):
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
        activity_summary = self.activity_summary(start, end)["activity"]
        return self.__summary_df(activity_summary, metrics)

    def activity_df_edited(self, start=None, end=None, metrics=None):
        """
        Create a dataframe from activity summary dict object.
        Some cols are unit converted for easier use or readability.

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        activity_df = self.activity_df_raw(start, end, metrics)
        return ActivityConverter().convert_metrics(activity_df)

    def readiness_df_raw(self, start=None, end=None, metrics=None):
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
        readiness_summary = self.readiness_summary(start, end)["readiness"]
        return self.__summary_df(readiness_summary, metrics)

    def readiness_df_edited(self, start=None, end=None, metrics=None):
        """
        Create a dataframe from ready summary dict object.
        Readiness has no cols to unit convert.

        :param start: Beginning of date range
        :type start: string representation of a date i.e. '2020-10-31'

        :param end: End of date range, or None if you want the current day.
        :type end: string representation of a date i.e. '2020-10-31'

        :param metrics: Metrics to include in the df.
        :type metrics: A list of strings, or a string
        """
        return self.readiness_df_raw(start, end, metrics)

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

        sleep_df = self.sleep_df_edited(start, end, metrics)
        sleep_df = prefix_cols(sleep_df, "SLEEP")
        readiness_df = self.readiness_df_edited(start, end, metrics)
        readiness_df = prefix_cols(readiness_df, "READY")
        activity_df = self.activity_df_edited(start, end, metrics)
        activity_df = prefix_cols(activity_df, "ACTIVITY")

        combined_df = sleep_df.merge(readiness_df, on="summary_date").merge(
            activity_df, on="summary_date"
        )
        return combined_df

    def save_as_xlsx(self, df, file, index=True, **to_excel_kwargs):
        """
        Save dataframe as .xlsx file with dates properly formatted

        :param df: dataframe to save
        :type df: df object

        :param file: File path
        :type file: string

        :param index: save df index, in this case summary_date
        :type index: Boolean
        """

        def localize(df):
            """
            Remove tz from datetime cols since Excel doesn't allow
            """
            tz_cols = df.select_dtypes(include=["datetimetz"]).columns
            for tz_col in tz_cols:
                df[tz_col] = df[tz_col].dt.tz_localize(None)
            return df

        import xlsxwriter

        df = df.copy()
        df = localize(df)
        writer = pd.ExcelWriter(
            file,
            engine="xlsxwriter",
            date_format="m/d/yyy",
            datetime_format="m/d/yyy h:mmAM/PM",
        )
        df.to_excel(writer, index=index, **to_excel_kwargs)
        writer.save()

    def tableize(self, df, tablefmt="pretty", is_print=True, filename=None):
        """
        Converts dataframe to a formatted table
        For more details, see https://pypi.org/project/tabulate/

        :param df: dataframe to save
        :type df: df object

        :param tablefmt: format of table
        :type tablefmt: string

        :param is_print: print to standard output?
        :type is_print: boolean

        :param filename: optionally, filename to print to
        :type filename: string
        """
        from tabulate import tabulate

        table = tabulate(
            df,
            headers="keys",
            tablefmt=tablefmt,
            showindex=True,
            stralign="center",
            numalign="center",
        )
        if is_print:
            print(table)
        if filename:
            with open(filename, "w") as f:
                print(table, file=f)
        return table


class UnitConverter:
    """
    Use this class to convert units for certain dataframe cols
    """

    all_dt_metrics = []
    all_sec_metrics = []

    def rename_converted_cols(self, df, metrics, suffix_str):
        """
        Rename converted cols by adding a suffix to the col name
        For example, 'bedtime_start' becomes 'bedtime_start_dt_adjusted'

        :param df: a dataframe
        :type df: pandas dataframe obj

        :param metrics: metrics to rename
        :type metrics: list of strings

        :param suffix_str: the str to append to each metric name
        :type suffix_str: str
        """
        updated_headers = [header + suffix_str for header in metrics]
        d_to_rename = dict(zip(metrics, updated_headers))
        df = df.rename(columns=d_to_rename)
        return df

    def convert_to_dt(self, df, dt_metrics):
        """
        Convert dataframe fields to datetime dtypes

        :param df: dataframe
        :type df: pandas dataframe obj

        :param dt_metrics: List of metrics to be converted to datetime
        :type dt_metrics: List
        """
        for i, dt_metric in enumerate(dt_metrics):
            df[dt_metric] = pd.to_datetime(df[dt_metric], format="%Y-%m-%d %H:%M:%S")
        df = self.rename_converted_cols(df, dt_metrics, "_dt_adjusted")
        return df

    def convert_to_hrs(self, df, sec_metrics):
        """
        Convert fields from seconds to minutes

        :param df: dataframe
        :type df: pandas dataframe obj

        :param sec_metrics: List of metrics to be converted from sec -> hrs
        :type sec_metrics: List
        """
        df[sec_metrics] = df[sec_metrics] / 60 / 60
        df = self.rename_converted_cols(df, sec_metrics, "_in_hrs")
        return df

    def convert_metrics(self, df):
        """
        Convert metrics to new unit type

        :param df: dataframe
        :type df: pandas dataframe obj
        """
        dt_metrics = [col for col in df.columns if col in self.all_dt_metrics]
        sec_metrics = [col for col in df.columns if col in self.all_sec_metrics]
        if dt_metrics:
            df = self.convert_to_dt(df, dt_metrics)
        if sec_metrics:
            df = self.convert_to_hrs(df, sec_metrics)
        return df


class SleepConverter(UnitConverter):
    all_dt_metrics = ["bedtime_end", "bedtime_start"]
    all_sec_metrics = [
        "awake",
        "deep",
        "duration",
        "light",
        "onset_latency",
        "rem",
        "total",
    ]


class ActivityConverter(UnitConverter):
    all_dt_metrics = ["day_end", "day_start"]
    all_sec_metrics = []
