import json

from . import OAuthRequestHandler, PersonalRequestHandler, exceptions


class OuraClient:
    """Use this class for making requests on behalf of a user. If refresh_token and
    expires_at are supplied, access_token should be refreshed automatically and
    passed to the refresh_callback function, along with other response properties.
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
        Initialize the client - requires either oauth credentials or a personal
        access token. Requests made using an instance will be done using a
        fixed "mode"

        :param client_id: The client id.
        :type client_id: str

        :param client_secret: The client secret. Required for auto refresh.
        :type client_secret: str

        :param access_token: Auth token.
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
        Returns information about the logged in user (who the access token was issued for).

        See https://cloud.ouraring.com/docs/personal-info
        """
        url = "{}/v1/userinfo".format(self.API_ENDPOINT)
        return self._make_request(url)

    def sleep_summary(self, start=None, end=None):
        """
        Get sleep summary for the given date range. See
        https://cloud.ouraring.com/docs/sleep

        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want the current day.
        :type end: date
        """
        url = self._build_summary_url(start, end, "sleep")
        return self._make_request(url)

    def activity_summary(self, start=None, end=None):
        """
        Get activity summary for the given date range.
        See https://cloud.ouraring.com/docs/activity

        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want the current day.
        :type end: date
        """
        url = self._build_summary_url(start, end, "activity")
        return self._make_request(url)

    def readiness_summary(self, start=None, end=None):
        """
        Get readiness summary for the given date range. See
        https://cloud.ouraring.com/docs/readiness

        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want the current day.
        :type end: date
        """
        url = self._build_summary_url(start, end, "readiness")
        return self._make_request(url)

    def bedtime_summary(self, start=None, end=None):
        """
        Get bedtime summary for the given date range. See
        https://cloud.ouraring.com/docs/bedtime

        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want the current day.
        :type end: date
        """
        url = self._build_summary_url(start, end, "bedtime")
        return self._make_request(url)

    def _make_request(self, url):
        response = self._auth_handler.make_request(url)

        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode("utf8"))
        return payload

    def _build_summary_url(self, start, end, datatype):
        if start is None:
            raise ValueError(
                "Request for {} summary must include start date.".format(datatype)
            )

        url = "{0}/v1/{1}?start={2}".format(self.API_ENDPOINT, datatype, start)
        if end:
            url = "{0}&end={1}".format(url, end)
        return url
