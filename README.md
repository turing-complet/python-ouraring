
## Installation

Package is on pypi, so install as follows, or clone the repo and install dependencies using pipenv.

`pip install oura` or `pipenv install oura`

## Getting started

Once you register an application, you can use this sample script to authorize access to your own data or some test account data. It will follow the auth code flow and print out the token response. Make sure to add localhost:3030 to the redirect uris for your app (the port can be changed in the script).
```
./token-request.py <client-id> <client-secret>
``` 

Some sample code is located in the [samples](samples) directory, maybe it will be useful for you. Maybe it will change your life for the better. Maybe it will cause you to rethink using this project at all. Let me know the outcome if you feel like it.


## Business time

If you are writing a real application, use the following pattern. Basically, the work is done by the underlying oauthlib to use the refresh token whenever the access token has expired, and you supply the refresh callback to save the new tokens for next time. This seems to have worked fine for me, but I don't actually use this library that much
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
# supply all the params for auto refresh
oura = OuraClient(<client_id>, <client_secret> <access_token>, <refresh_token>, <refresh_callback>)

# or just these for make calls until token expires
oura = OuraClient(<client_id>, <access_token>)

# make authenticated API calls
oura.user_info()
oura.sleep_summary(start='2018-12-05', end='2018-12-10')
oura.activity_summary(start='2018-12-25')
oura.readiness_summary() # throws exception since start is None
```


The `refresh_callback` is a fuction that takes a token dict and saves it somewhere. It will look like:
```
{'token_type': 'bearer', 'refresh_token': <refresh>, 'access_token': <token>, 'expires_in': 86400, 'expires_at': 1546485086.3277025}
```

Live your life.
