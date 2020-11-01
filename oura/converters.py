import pandas as pd


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
