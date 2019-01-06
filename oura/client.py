
from requests_oauthlib import OAuth2Session
from . import exceptions
import json
import requests

class OuraOAuth2Client:

    AUTHORIZE_BASE_URL = "https://cloud.ouraring.com/oauth/authorize"
    TOKEN_BASE_URL = "https://api.ouraring.com/oauth/token"
    SCOPE = ["email", "personal", "daily"]

    def __init__(self, client_id, client_secret):

        """
        Use this for authorizing user and obtaining initial access and refresh token.
        Should be one time usage per user.

        :param client_id: The client id from oura portal.
        :type client_id: str
        :param client_secret: The client secret from oura portal.
        :type client_secret: str
        """
        self.client_id = client_id
        self.client_secret = client_secret

        self.session = OAuth2Session(
            client_id,
            auto_refresh_url=self.TOKEN_BASE_URL,
        )


    def authorize_endpoint(self, scope=None, redirect_uri=None, **kwargs):
        self.session.scope = scope or self.SCOPE
        if redirect_uri:
            self.session.redirect_uri = redirect_uri
        return self.session.authorization_url(self.AUTHORIZE_BASE_URL, **kwargs)


    def fetch_access_token(self, code):
        return self.session.fetch_token(
            self.TOKEN_BASE_URL,
            code=code,
            client_secret = self.client_secret)


class OuraClient:
    """
    Use this class for making requests on behalf ot a user. If refresh_token and expires_at are supplied, 
    access_token should be refreshed automatically and passed to the refresh_callback function, along with
    other properties in the response.
    """

    API_ENDPOINT = "https://api.ouraring.com"
    TOKEN_BASE_URL = "https://api.ouraring.com/oauth/token"

    def __init__(self, client_id, access_token=None, refresh_token=None,
        expires_at=None, refresh_callback=None):

        """
        Initialize the client

        :param client_id: The client id from oura portal.
        :type client_id: str

        :param access_token: Auth token.
        :type access_token: str

        :param refresh_token: Use this to renew tokens when they expire
        :type refresh_token: str

        :param expires_at: The unix timestamp for access token expiration.
        :type expires_at: str

        :param refresh_callback: Method to save the access token, refresh token, expires at
        :type refresh_callback: callable

        """

        token = {}
        if access_token:
            token.update({ 'access_token': access_token })
        if refresh_token:
            token.update({ 'refresh_token': refresh_token })
        if expires_at:
            token['expires_at'] = expires_at

        self._session = OAuth2Session(
            client_id,
            token=token,
            auto_refresh_url=self.TOKEN_BASE_URL,
            token_updater=refresh_callback
        )


    def user_info(self):
        """
        Returns information about the logged in user (who the access token was issued for).

        See https://cloud.ouraring.com/docs/personal-info
        """
        url = "{}/v1/userinfo".format(self.API_ENDPOINT)
        return self._make_request(url)

    
    def sleep_summary(self, start=None, end=None):
        url = self._build_summary_url(start, end, "sleep")
        return self._make_request(url)


    def activity_summary(self, start=None, end=None):
        url = self._build_summary_url(start, end, "activity")
        return self._make_request(url)


    def readiness_summary(self, start=None, end=None):
        url = self._build_summary_url(start, end, "readiness")
        return self._make_request(url)


    def _make_request(self, url, data=None, method=None, **kwargs):
        data = data or {}
        method = method or 'GET'
        response = self._session.request(
            method,
            url,
            data=data,
            **kwargs
        )
        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode('utf8'))
        return payload

    def _build_summary_url(self, start, end, datatype):
        if start is None:
            raise ValueError("Request for {} summary must include start date.".format(datatype))

        url = "{0}/v1/{1}?start={2}".format(self.API_ENDPOINT, datatype, start)
        if end:
            url = "{0}&end={1}".format(url, end)
        return url