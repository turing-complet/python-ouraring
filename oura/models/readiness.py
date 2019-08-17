
from helper import OuraModel, from_json

class Readiness(OuraModel):
    _KEYS = [
        "summary_date",
        "period_id",
        "score",
        "score_previous_night",
        "score_sleep_balance",
        "score_previous_day",
        "score_activity_balance",
        "score_resting_hr",
        "score_recovery_index",
        "score_temperature"
    ]


if __name__  == '__main__':
    test = """
{
        "summary_date": "2016-09-03",
        "period_id": 0,
        "score": 62,
        "score_previous_night": 5,
        "score_sleep_balance": 75,
        "score_previous_day": 61,
        "score_activity_balance": 77,
        "score_resting_hr": 98,
        "score_recovery_index": 45,
        "score_temperature": 86
}"""

    readiness = from_json(test, Readiness)
    print(readiness)