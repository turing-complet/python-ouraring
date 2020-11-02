import json

from . import OAuthRequestHandler, PersonalRequestHandler, exceptions


class OuraClient:
    """Make requests to Oura's API. Provide either oauth client and token
    information to make requests on behalf of users, or a personal access token
    to access your own data.
    """

    API_ENDPOINT = "https://api.ouraring.com"

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

    def user_info(self):
        """
        Returns information about the current user.

        See https://cloud.ouraring.com/docs/personal-info
        """
        url = "{}/v1/userinfo".format(self.API_ENDPOINT)
        return self._make_request(url)

    def sleep_summary(self, start=None, end=None):
        """
        Get sleep summary for the given date range. See
        https://cloud.ouraring.com/docs/sleep

        :param start: Beginning of date range, YYYY-MM-DD
        :type start: str

        :param end: End of date range, or None if you want the current day.
        :type end: str, optional
        """
        return self._get_summary(start, end, "sleep")

    def activity_summary(self, start=None, end=None):
        """
        Get activity summary for the given date range.
        See https://cloud.ouraring.com/docs/activity

        :param start: Beginning of date range, YYYY-MM-DD
        :type start: str

        :param end: End of date range, or None if you want the current day.
        :type end: str, optional
        """
        return self._get_summary(start, end, "activity")

    def readiness_summary(self, start=None, end=None):
        """
        Get readiness summary for the given date range. See
        https://cloud.ouraring.com/docs/readiness

        :param start: Beginning of date range, YYYY-MM-DD
        :type start: str

        :param end: End of date range, or None if you want the current day.
        :type end: str, optional
        """
        return self._get_summary(start, end, "readiness")

    def bedtime_summary(self, start=None, end=None):
        """
        Get bedtime summary for the given date range. See
        https://cloud.ouraring.com/docs/bedtime

        :param start: Beginning of date range, YYYY-MM-DD
        :type start: str

        :param end: End of date range, or None if you want the current day.
        :type end: str, optional
        """
        return self._get_summary(start, end, "bedtime")

    def _get_summary(self, start, end, summary_type):
        url = self._build_summary_url(start, end, summary_type)
        return self._make_request(url)

    def _make_request(self, url):
        response = self._auth_handler.make_request(url)
        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode("utf8"))
        return payload

    def _build_summary_url(self, start, end, summary_type):
        url = "{0}/v1/{1}".format(self.API_ENDPOINT, summary_type)
        params = {}
        if start is not None:
            if not isinstance(start, str):
                raise TypeError("start date must be of type str")
            params["start"] = start

        if end is not None:
            if not isinstance(end, str):
                raise TypeError("end date must be of type str")
            params["end"] = end

        qs = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{qs}"
        return url
