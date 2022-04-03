import json

from .. import exceptions
from ..auth import PersonalRequestHandler


class OuraV2:

    API_ENDPOINT = "https://api.ouraring.com/v2/usercollection"

    def __init__(self, personal_access_token) -> None:
        if personal_access_token is not None:
            self._auth_handler = PersonalRequestHandler(personal_access_token)

    def daily_activity(self, start_date=None, end_date=None, next_token=None):
        # end_date default to current UTC date
        # start_date default to end_date - 1 day
        return self._get_summary(start_date, end_date, next_token, "daily_activity")

    def heartrate(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "heartrate")

    def personal_info(self):
        url = f"{self.API_ENDPOINT}/personal_info"
        return self._make_request(url)

    def session(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "session")

    def tags(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "tag")

    def workouts(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "workout")

    def _get_summary(self, start_date, end_date, next_token, summary_type):
        url = self._build_summary_url(start_date, end_date, next_token, summary_type)
        return self._make_request(url)

    def _make_request(self, url):
        print(url)
        response = self._auth_handler.make_request(url)
        # return response
        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode("utf8"))
        return payload

    def _build_summary_url(self, start_date, end_date, next_token, summary_type):
        url = f"{self.API_ENDPOINT}/{summary_type}"
        params = {}
        if start_date is not None:
            if not isinstance(start_date, str):
                raise TypeError("start date must be of type str")
            params["start_date"] = start_date

        if end_date is not None:
            if not isinstance(end_date, str):
                raise TypeError("end date must be of type str")
            params["end_date"] = end_date

        if next_token is not None:
            params["next_token"] = next_token

        qs = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{qs}" if qs != "" else url
        return url
