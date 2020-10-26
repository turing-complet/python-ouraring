from oura import OuraClient, OuraClientDataFrame


class MockClient(OuraClient):
    def user_info(self):
        return {
            "age": 27,
            "weight": 80,
            "gender": "male",
            "email": "john.doe@the.domain",
        }

    def activity_summary(self, start=None, end=None):
        minutes_per_day = 1440
        return {
            "activity": [
                {
                    "summary_date": "2016-09-03",
                    "day_start": "2016-09-03T04:00:00+03:00",
                    "day_end": "2016-09-04T03:59:59+03:00",
                    "timezone": 180,
                    "score": 87,
                    "score_stay_active": 90,
                    "score_move_every_hour": 100,
                    "score_meet_daily_targets": 60,
                    "score_training_frequency": 96,
                    "score_training_volume": 95,
                    "score_recovery_time": 100,
                    "daily_movement": 7806,
                    "non_wear": 313,
                    "rest": 426,
                    "inactive": 429,
                    "inactivity_alerts": 0,
                    "low": 224,
                    "medium": 49,
                    "high": 0,
                    "steps": 9206,
                    "cal_total": 2540,
                    "cal_active": 416,
                    "met_min_inactive": 9,
                    "met_min_low": 167,
                    "met_min_medium_plus": 159,
                    "met_min_medium": 159,
                    "met_min_high": 0,
                    "average_met": 1.4375,
                    "class_5min": "1112211111111111111111111111111111111111111111233322322223333323322222220000000000000000000000000000000000000000000000000000000233334444332222222222222322333444432222222221230003233332232222333332333333330002222222233233233222212222222223121121111222111111122212321223211111111111111111",
                    "met_1min": [0.9] * minutes_per_day,
                    "rest_mode_state": 0,
                }
            ]
        }

    def sleep_summary(self, start=None, end=None):
        return {
            "sleep": [
                {
                    "summary_date": "2017-11-05",
                    "period_id": 0,
                    "is_longest": 1,
                    "timezone": 120,
                    "bedtime_start": "2017-11-06T02:13:19+02:00",
                    "bedtime_end": "2017-11-06T08:12:19+02:00",
                    "score": 70,
                    "score_total": 57,
                    "score_disturbances": 83,
                    "score_efficiency": 99,
                    "score_latency": 88,
                    "score_rem": 97,
                    "score_deep": 59,
                    "score_alignment": 31,
                    "total": 20310,
                    "duration": 21540,
                    "awake": 1230,
                    "light": 10260,
                    "rem": 7140,
                    "deep": 2910,
                    "onset_latency": 480,
                    "restless": 39,
                    "efficiency": 94,
                    "midpoint_time": 11010,
                    "hr_lowest": 49,
                    "hr_average": 56.375,
                    "rmssd": 54,
                    "breath_average": 13,
                    "temperature_delta": -0.06,
                    "hypnogram_5min": "443432222211222333321112222222222111133333322221112233333333332232222334",
                    "hr_5min": [52] * 72,
                    "rmssd_5min": [61] * 72,
                }
            ]
        }

    def readiness_summary(self, start=None, end=None):
        return {
            "readiness": [
                {
                    "summary_date": "2016-09-03",
                    "period_id": 0,
                    "score": 62,
                    "score_previous_night": 5,
                    "score_sleep_balance": 75,
                    "score_previous_day": 61,
                    "score_activity_balance": 77,
                    "score_resting_hr": 98,
                    "score_hrv_balance": 90,
                    "score_recovery_index": 45,
                    "score_temperature": 86,
                    "rest_mode_state": 0,
                }
            ]
        }

    def bedtime_summary(self, start=None, end=None):
        return {
            "ideal_bedtimes": [
                {
                    "date": "2020-03-17",
                    "bedtime_window": {"start": -3600, "end": 0},
                    "status": "IDEAL_BEDTIME_AVAILABLE",
                },
                {
                    "date": "2020-03-18",
                    "bedtime_window": {"start": None, "end": None},
                    "status": "LOW_SLEEP_SCORES",
                },
            ]
        }


class MockDataFrameClient(OuraClientDataFrame, MockClient):
    pass
