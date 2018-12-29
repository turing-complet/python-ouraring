Usage:

Run the following to go through the auth code flow (will launch a browser) which will print an access and refresh token.
```
./token-request.py <client-id> <client-secret>
``` 

In python, do
```
# use token from the script output
oura = OuraClient(<client-id>, <client-secret>, <access-token>, <refresh-token>)

# make authenticated API calls
oura.user_info()
oura.sleep_summary(start='2018-12-05', end='2018-12-10')
oura.activity_summary(start='2018-12-25')
oura.readiness_summary() # throws exception since start is None
```

Live your life.
