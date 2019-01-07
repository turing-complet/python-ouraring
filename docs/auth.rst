.. _auth:

Authentication and Authorization
********************************

Oura uses OAuth2 to allow a user to grant access to their data.

See the `official documentation <https://cloud.ouraring.com/docs/authentication>`_

Requesting Authorization
========================

The :class:`oura.OuraOAuth2Client` class has an :meth:`authorize_endpoint` method
which returns a url that a user can click to grant access. 

This can be called as follows::

    from oura import OuraOAuth2Client
    auth_client = OuraOAuth2Client(client_id=MY_CLIENT_ID, client_secret=SUPER_SECRET_VALUE)
    url = auth_client.authorize_endpoint(scope = ["email", "personal", "daily"], redirect_uri='http://my.domain.com/callback')


In following the standard flow, you would have some code under your `/callback` endpoint that does this ::

    code = request.args.get('code') # e.g.
    token_response = auth_client.fetch_access_token(code=code)


Now you are ready to make authenticated API requests. Please use this power responsibly.