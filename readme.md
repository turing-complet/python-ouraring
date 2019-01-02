Usage:

Run the following to go through the auth code flow (will launch a browser) which will print an access and refresh token.
```
./token-request.py <client-id> <client-secret>
``` 

In python, do
```
oura = OuraClient(<client-id>, <client-secret>, <access-token>, <refresh-token>, <refresh-callback>, <expires-at>)

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
