from oura.v2 import OuraClientDataFrameV2, OuraClientV2


class MockClientV2(OuraClientV2):
    def personal_info(self):
        return {
            "age": 31,
            "weight": 74.8,
            "height": 1.8,
            "biological_sex": "male",
            "email": "example@example.com",
        }

    def daily_activity(self, start_date=None, end_date=None, next_token=None):
        return {
            "data": [
                {
                    "class_5_min": "000000000000000000000000000000000000000000000000000000000000000000000000003444544444445545455443454554454443334333322330000000000232232222222232222222322223222000000022332233422333222232233333222222222222222332223212233222122221111111111111121111111111111111111111111111111111111111111111",
                    "score": 82,
                    "active_calories": 1222,
                    "average_met_minutes": 1.90625,
                    "contributors": {
                        "meet_daily_targets": 43,
                        "move_every_hour": 100,
                        "recovery_time": 100,
                        "stay_active": 98,
                        "training_frequency": 71,
                        "training_volume": 98,
                    },
                    "equivalent_walking_distance": 20122,
                    "high_activity_met_minutes": 444,
                    "high_activity_time": 3000,
                    "inactivity_alerts": 0,
                    "low_activity_met_minutes": 117,
                    "low_activity_time": 10020,
                    "medium_activity_met_minutes": 391,
                    "medium_activity_time": 6060,
                    "met": {
                        "interval": 60,
                        "items": [  # truncated for readability
                            0.1,
                            0.1,
                            0.1,
                            0.1,
                            0.9,
                            0.9,
                            0.9,
                            0.1,
                            0.1,
                            0.1,
                            0.1,
                            0.1,
                            0.9,
                            0.9,
                            0.9,
                            0.9,
                            0.9,
                            0.9,
                            0.9,
                        ],
                        "timestamp": "2021-11-26T04:00:00.000-08:00",
                    },
                    "meters_to_target": -16200,
                    "non_wear_time": 27480,
                    "resting_time": 18840,
                    "sedentary_met_minutes": 10,
                    "sedentary_time": 21000,
                    "steps": 18430,
                    "target_calories": 350,
                    "target_meters": 7000,
                    "total_calories": 3446,
                    "day": "2021-11-26",
                    "timestamp": "2021-11-26T04:00:00-08:00",
                }
            ],
            "next_token": None,
        }

    def heartrate(self, start_date=None, end_date=None, next_token=None):
        return {
            "data": [
                {"bpm": 60, "source": "sleep", "timestamp": "2021-01-01T01:02:03+00:00"}
            ],
            "next_token": None,
        }

    def session(self, start_date=None, end_date=None, next_token=None):
        return {
            "data": [
                {
                    "day": "2021-11-12",
                    "start_datetime": "2021-11-12T12:32:09-08:00",
                    "end_datetime": "2021-11-12T12:40:49-08:00",
                    "type": "rest",
                    "heart_rate": None,
                    "heart_rate_variability": None,
                    "mood": None,
                    "motion_count": {
                        "interval": 5,
                        "items": [0],
                        "timestamp": "2021-11-12T12:32:09.000-08:00",
                    },
                }
            ],
            "next_token": None,
        }

    def tags(self, start_date=None, end_date=None, next_token=None):
        return {
            "data": [
                {
                    "day": "2021-01-01",
                    "text": "Need coffee",
                    "timestamp": "2021-01-01T01:02:03-08:00",
                    "tags": ["tag_generic_nocaffeine"],
                }
            ],
            "next_token": None,
        }

    def workouts(self, start_date=None, end_date=None, next_token=None):
        return {
            "data": [
                {
                    "activity": "cycling",
                    "calories": 300,
                    "day": "2021-01-01",
                    "distance": 13500.5,
                    "end_datetime": "2021-01-01T01:00:00.000000+00:00",
                    "intensity": "moderate",
                    "label": None,
                    "source": "manual",
                    "start_datetime": "2021-01-01T01:30:00.000000+00:00",
                }
            ],
            "next_token": None,
        }


class MockDataFrameClientV2(OuraClientDataFrameV2, MockClientV2):
    pass
