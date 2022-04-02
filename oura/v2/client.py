from ..auth import PersonalRequestHandler


class OuraV2:

    API_ENDPOINT = "https://api.ouraring.com/v2/usercollection"

    def __init__(self, personal_access_token) -> None:
        if personal_access_token is not None:
            self._auth_handler = PersonalRequestHandler(personal_access_token)

    def daily_activity(self, start_date, end_date, next_token=None):
        # end_date default to current UTC date
        # start_date default to end_date - 1 day
        pass

    def heartrate(self, start_date, end_date, next_token=None):
        pass

    def personal_info(self):
        pass

    def session(self, start_date, end_date, next_token=None):
        pass

    def tags(self, start_date, end_date, next_token=None):
        # url is /tag
        pass

    def workouts(self, start_date, end_date, next_token=None):
        # url is /workout
        pass
