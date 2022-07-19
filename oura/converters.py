import pandas as pd


class UnitConverter:
    """
    Use this class to convert units for certain dataframe cols

    :param convert_cols: A set of columns to apply predefined conversions
    :type convert_cols: list/set
    """

    all_dt_metrics = []
    all_sec_metrics = []
    all_metrics = all_dt_metrics + all_sec_metrics

    def __init__(self, convert_cols=None):
        if convert_cols is not None:
            convert_cols = set(convert_cols)
            defaults = set(self.all_metrics)
            invalid = convert_cols - defaults
            if any(invalid):
                print(f"Ignoring metrics with no conversion: {invalid}")
            self.convert_cols = list(convert_cols & defaults)
        else:
            self.convert_cols = self.all_metrics

    def _rename_converted_cols(self, df, metrics, suffix_str):
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

    def _convert_to_dt(self, df, dt_metrics):
        """
        Convert dataframe fields to datetime dtypes

        :param df: dataframe
        :type df: pandas dataframe obj

        :param dt_metrics: List of metrics to be converted to datetime
        :type dt_metrics: List
        """
        for _, dt_metric in enumerate(dt_metrics):
            df[dt_metric] = pd.to_datetime(df[dt_metric], format="%Y-%m-%d %H:%M:%S")
        df = self._rename_converted_cols(df, dt_metrics, "_dt_adjusted")
        return df

    def _convert_to_hrs(self, df, sec_metrics):
        """
        Convert fields from seconds to minutes

        :param df: dataframe
        :type df: pandas dataframe obj

        :param sec_metrics: List of metrics to be converted from sec -> hrs
        :type sec_metrics: List
        """
        df[sec_metrics] = df[sec_metrics] / 60 / 60
        df = self._rename_converted_cols(df, sec_metrics, "_in_hrs")
        return df

    def _select_cols(self, df, subset):
        return [c for c in df.columns if c in set(subset) & set(self.convert_cols)]

    def convert_metrics(self, df):
        """
        Convert metrics to new unit type

        :param df: dataframe
        :type df: pandas dataframe obj
        """
        dt_metrics = self._select_cols(df, self.all_dt_metrics)
        df = self._convert_to_dt(df, dt_metrics)

        sec_metrics = self._select_cols(df, self.all_sec_metrics)
        df = self._convert_to_hrs(df, sec_metrics)
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
    hypnogram_5min = ["hypnogram_5min"]
    all_metrics = all_dt_metrics + all_sec_metrics + hypnogram_5min

    def convert_hypnogram_helper(self, hypnogram):
        d = {"1": "D", "2": "L", "3": "R", "4": "A"}
        return "".join(list(map(lambda h: d[h], hypnogram)))

    def convert_hypnogram(self, sleep_df):
        if "hypnogram_5min" in sleep_df.columns:
            sleep_df["hypnogram_5min"] = sleep_df["hypnogram_5min"].apply(
                self.convert_hypnogram_helper
            )
        return sleep_df

    def convert_metrics(self, df):
        df = super().convert_metrics(df)
        if "hypnogram_5min" in self.convert_cols:
            df = self.convert_hypnogram(df)
        return df


class ActivityConverter(UnitConverter):
    all_dt_metrics = ["day_end", "day_start"]
    all_metrics = all_dt_metrics
