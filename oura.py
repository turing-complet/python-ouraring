
from requests_oauthlib import OAuth2Session
import exceptions
import json

class OuraOAuth2Client:

    AUTHORIZE_BASE_URL = "https://cloud.ouraring.com/oauth/authorize"
    TOKEN_BASE_URL = "https://api.ouraring.com/oauth/token"
    SCOPE = ["email", "personal", "daily"]

    def __init__(self, client_id, client_secret, access_token=None,
        refresh_token=None, expires_at=None, refresh_cb=None,
        redirect_uri=None, *args, **kwargs):

        self.client_id, self.client_secret = client_id, client_secret
        token = {}
        if access_token and refresh_token:
            token.update({
                'access_token': access_token,
                'refresh_token': refresh_token
            })
        if expires_at:
            token['expires_at'] = expires_at
        self.session = OAuth2Session(
            client_id,
            token=token,
            redirect_uri=redirect_uri
        )
        self.timeout = kwargs.get("timeout", None)


    def _request(self, method, url, **kwargs):

        if self.timeout is not None and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.Timeout as e:
            raise exceptions.Timeout(*e.args)


    def make_request(self, url, data=None, method=None, **kwargs):
        data = data or {}
        method = method or ('POST' if data else 'GET')
        response = self._request(
            method,
            url,
            data=data,
            client_id=self.client_id,
            client_secret=self.client_secret,
            **kwargs
        )

        exceptions.detect_and_raise_error(response)
        return response


    def authorize_endpoint(self, scope=None, redirect_uri=None, **kwargs):
        self.session.scope = scope or self.SCOPE
        if redirect_uri:
            self.session.redirect_uri = redirect_uri
        return self.session.authorization_url(self.AUTHORIZE_BASE_URL, **kwargs)


    def fetch_access_token(self, code, redirect_uri=None):
        if redirect_uri:
            self.session.redirect_uri = redirect_uri
        return self.session.fetch_token(
            self.TOKEN_BASE_URL,
            username=self.client_id,
            password=self.client_secret,
            code=code)


class OuraClient:

    API_ENDPOINT = "https://api.ouraring.com"

    def __init__(self, client_id, client_secret, access_token=None, 
        refresh_token=None, expires_at=None, redirect_uri=None, **kwargs):

        self.client = OuraOAuth2Client(
            client_id,
            client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            redirect_uri=redirect_uri,
            **kwargs
        )


    def make_request(self, *args, **kwargs):
        # This should handle data level errors, improper requests, and bad
        # serialization
        headers = kwargs.get('headers', {})
        kwargs['headers'] = headers

        method = kwargs.get('method', 'POST' if 'data' in kwargs else 'GET')
        response = self.client.make_request(*args, **kwargs)

        if response.status_code == 202:
            return True
        if method == 'DELETE':
            if response.status_code == 204:
                return True
            else:
                raise exceptions.DeleteError(response)
        try:
            rep = json.loads(response.content.decode('utf8'))
        except ValueError:
            raise exceptions.BadResponse

        return rep


    def user_info(self):
        url = "{}/v1/userinfo".format(self.API_ENDPOINT)
        return self.make_request(url)

    
    def sleep_summary(self, start=None, end=None):
        url = self._build_summary_url(start, end, "sleep")
        return self.make_request(url)


    def activity_summary(self, start=None, end=None):
        url = self._build_summary_url(start, end, "activity")
        return self.make_request(url)


    def readiness_summary(self, start=None, end=None):
        url = self._build_summary_url(start, end, "readiness")
        return self.make_request(url)


    def _build_summary_url(self, start, end, datatype):
        if start is None:
            raise ValueError("Request for {} summary must include start date.".format(datatype))

        url = "{0}/v1/{1}?start={2}".format(self.API_ENDPOINT, datatype, start)
        if end:
            url = "{0}&end={1}".format(url, end)
        return url