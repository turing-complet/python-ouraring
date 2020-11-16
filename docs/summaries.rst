.. _summaries:

Daily summaries
********************************

Oura's API is based on the idea of daily summaries. For each kind of data (sleep, activity, readiness, bedtime)
there is an endpoint which will return summaries for one or more day. They each
take an optional start date and end date (YYYY-MM-DD).

See the `official documentation <https://cloud.ouraring.com/docs/daily-summaries>`_ for behavior regarding the dates.

Usage
========================

If you just want to make some requests, it's fairly easy. Just do this ::

    from oura import OuraClient
    oura = OuraClient(client_id=MY_CLIENT_ID, access_token=ACCESS_TOKEN)

And you're set to call summary methods.


If you want a more automated approach, your application should implement a way to store and retrieve the token information for each user, 
and create each instance of :class:`oura.OuraClient` with that information (as well the client_id to identify your app).

For example::

    from oura import OuraClient
    token = get_token_from_database(some_user_id) # you implement this
    access_token = token['access_token']
    refresh_token = token['refresh_token']

    # you implement save_token_to_db() function
    client = OuraClient(client_id=MY_CLIENT_ID, client_secret=MY_CLIENT_SECRET, access_token, refresh_token, refresh_callback=save_token_to_db)


Now you are ready to get all the data, provided the user has granted you the required scopes. ::

    from datetime import date
    today = str(date.today()) # 2019-01-06, e,g, YYYY-MM-DD, or use whatever start/end date you want
    sleep_summary = client.sleep_summary(start=today)


