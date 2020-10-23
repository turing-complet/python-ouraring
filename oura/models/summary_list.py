import json
from helper import OuraModel, from_json, from_dict, set_attrs
from datetime import datetime
from sleep import Sleep
from activity import Activity
from readiness import Readiness


class OuraSummary:
    def __init__(self, summary_dict):
        self.summary_dict = summary_dict
        set_attrs(self, json.loads(summary_dict))

    def _by_date(self, typename):

        result = {}  # date -> OuraModel object

        for item in self.summary_dict:

            # parse item into an OuraModel so it has summary_date defined
            obj = typename(json_parsed=item)
            summary_date = obj.summary_date
            date_obj = datetime.strptime(summary_date, "%Y-%m-%d").date()

            result[date_obj] = obj

        return result


class SleepSummary(OuraSummary, OuraModel):
    _KEYS = ["sleep"]

    def by_date(self):
        return self._by_date(Sleep)


class ActivitySummary(OuraSummary, OuraModel):
    _KEYS = ["activity"]

    def by_date(self):
        return self._by_date(Activity)


class ReadinessSummary(OuraSummary, OuraModel):
    _KEYS = ["readiness"]

    def by_date(self):
        return self._by_date(Readiness)


if __name__ == "__main__":
    test = """
{
    "readiness" : [
        {
            "summary_date": "2016-09-03",
            "period_id": "0",
            "score": "62",
            "score_previous_night": "5",
            "score_sleep_balance": "75",
            "score_previous_day": "61",
            "score_activity_balance": "77",
            "score_resting_hr": "98",
            "score_recovery_index": "45",
            "score_temperature": "86"
        }
    ]
}"""

    summary = ReadinessSummary(test)
    print(summary.by_date())
