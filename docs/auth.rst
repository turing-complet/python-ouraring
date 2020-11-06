.. _auth:

Authentication and Authorization
********************************

There are two choices for auth:

* oauth2 for making requests on behalf of other users
* personal access tokens, which are unsurprisingly for personal use


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

Personal Access Token
=====================

You can also access your own data using a personal_access_token - get one from
the cloud portal and save the value somewhere, like an environment variable. Or
somewhere else, it's your token anyway. Then just pass it to a new
:class:`oura.OuraClient` instance and you'll be ready to go. See what I mean ::

    import os
    from oura import OuraClient
    my_token = os.getenv('MY_TOKEN')
    client = OuraClient(personal_access_token=my_token)
    who_am_i = client.user_info()

