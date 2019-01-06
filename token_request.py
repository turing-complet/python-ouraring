#!/usr/bin/env python
import os
import sys
import threading
import webbrowser
from oura import OuraOAuth2Client
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    auth_code = request.args.get('code')
    try:
        auth_client.fetch_access_token(auth_code)
        print("Save these values!")
        for key, value in auth_client.session.token.items():
            print('{} = {}'.format(key, value))
        return "<h1>You are now authorized to access the Oura API!</h1>"
    except Exception as e:
        print(e)
        return "<h1>Error retrieving a token {}</h1>".format(e)


def browser_authorize(auth_client):
    url, _ = auth_client.authorize_endpoint()
    threading.Timer(1, webbrowser.open, args=(url,)).start()


if __name__ == '__main__':

    if not (len(sys.argv) == 3):
        print("Arguments: client_id and client_secret")
        sys.exit(1)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    auth_client = OuraOAuth2Client(*sys.argv[1:])
    browser_authorize(auth_client)

    # test_response = server.oura.user_info()
    app.run(debug = False, host='0.0.0.0', port=3030)
    
    input("Press any key to close")
