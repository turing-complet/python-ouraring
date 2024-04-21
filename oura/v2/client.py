import json
from urllib.parse import urlencode

from .. import exceptions
from ..auth import OAuthRequestHandler, PersonalRequestHandler


class OuraClientV2:

    API_ENDPOINT = "https://api.ouraring.com/v2/usercollection"

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        access_token=None,
        refresh_token=None,
        refresh_callback=None,
        personal_access_token=None,
    ):
        """
        :param client_id: The client id - identifies your application.
        :type client_id: str

        :param client_secret: The client secret. Required for auto refresh.
        :type client_secret: str

        :param access_token: Access token.
        :type access_token: str

        :param refresh_token: Use this to renew tokens when they expire
        :type refresh_token: str

        :param refresh_callback: Callback to handle token response
        :type refresh_callback: callable

        :param personal_access_token: Token used for accessing personal data
        :type personal_access_token: str
        """

        if client_id is not None:
            self._auth_handler = OAuthRequestHandler(
                client_id, client_secret, access_token, refresh_token, refresh_callback
            )

        if personal_access_token is not None:
            self._auth_handler = PersonalRequestHandler(personal_access_token)

    def daily_activity(self, start_date=None, end_date=None, next_token=None):
        # end_date default to current UTC date
        # start_date default to end_date - 1 day
        return self._get_summary(start_date, end_date, next_token, "daily_activity")

    def daily_readiness(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "daily_readiness")

    def daily_sleep(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "daily_sleep")

    def daily_spo2(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "daily_spo2")

    def daily_stress(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "daily_stress")

    def enhanced_tag(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "enhanced_tag")

    def heartrate(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "heartrate")

    def personal_info(self):
        return self._get_summary(None, None, None, "personal_info")

    def rest_mode_period(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "rest_mode_period")

    def ring_configuration(self, next_token=None):
        return self._get_summary(None, None, next_token, "ring_configuration")

    def session(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "session")

    def sleep(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "sleep")

    def sleep_time(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "sleep_time")

    def workouts(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "workout")

    def _get_summary(self, start_date, end_date, next_token, summary_type):
        url = self._build_summary_url(start_date, end_date, next_token, summary_type)
        return self._make_request(url)

    def _make_request(self, url):
        response = self._auth_handler.make_request_v2(url)
        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode("utf8"))
        return payload

    def _build_summary_url(self, start_date, end_date, next_token, summary_type):
        url = f"{self.API_ENDPOINT}/{summary_type}"
        params = {}
        if start_date is not None:
            if not isinstance(start_date, str):
                raise TypeError("start date must be of type str")
            key = "start_datetime" if summary_type == 'heartrate' else "start_date"
            params[key] = start_date

        if end_date is not None:
            if not isinstance(end_date, str):
                raise TypeError("end date must be of type str")
            key = "end_datetime" if summary_type == 'heartrate' else "end_date"
            params[key] = end_date

        if next_token is not None:
            params["next_token"] = next_token

        qs = urlencode(params)
        url = f"{url}?{qs}" if qs != "" else url
        return url

    def revoke_token(self):
        response = self._auth_handler.revoke_token()
        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode("utf8"))
        return payload
