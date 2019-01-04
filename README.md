Better docs coming soon..

Usage:

Run the following to go through the auth code flow (will launch a browser) which will print an access and refresh token.
```
./token-request.py <client-id> <client-secret>
``` 

In python, do
```
from oura import OuraClient, OuraOAuth2Client

auth_client = OuraOAuth2Client(client_id='my_application', client_secret='random-string')
url = auth_client.authorize_endpoint(scope='defaults to all scopes', 'https://localhost/myendpoint')
# user clicks url, auth happens, then redirect to given url
```

Now we handle the redirect by exchanging an auth code for a token

```
# save this somewhere, see below
token_dict = auth_client.fetch_access_token(code='auth_code_from_query_string')
```

Now that's out of the way, you can call the api:
```
oura = OuraClient(client_id='my_application', <access-token>, <refresh-token>, <expires-at>, <refresh-callback>)

# make authenticated API calls
oura.user_info()
oura.sleep_summary(start='2018-12-05', end='2018-12-10')
oura.activity_summary(start='2018-12-25')
oura.readiness_summary() # throws exception since start is None
```

Constructor arguments `access-token`, `refresh-token`, and `expires-at` should be stored per user and passed in to allow auto-renewal

The `refresh-callback` is a fuction that takes a token dict and saves it somewhere. It will look like:
```
{'token_type': 'bearer', 'refresh_token': <refresh>, 'access_token': <token>, 'expires_in': 86400, 'expires_at': 1546485086.3277025}
```

Live your life.