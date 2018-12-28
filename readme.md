Usage:

Run the following to go through the auth code flow and print a token.
```
./token-request.py <client-id> <client-secret>
``` 

In python, do
```
# use token from the script output
oura = OuraClient(<client-id>, <client-secret>, <access-token>)

# make authenticated API calls
oura.user_info()
oura.sleep_summary('2018-12-05', '2018-12-10')
```

Live your life.