#!/usr/bin/env python
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser

from base64 import b64encode
from oura import OuraClient, OuraOAuth2Client
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError


class OAuth2Server:
    def __init__(self, client_id, client_secret):

        self.success_html = """
            <h1>You are now authorized to access the Oura API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.oura = OuraClient(client_id, client_secret)


    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.oura.client.authorize_endpoint()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        cherrypy.config.update({'server.socket_port': 3030})
        cherrypy.quickstart(self)


    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Oura response containing a verification code. Use the code
        to fetch the access_token.
        """
        if code:
            try:
                self.oura.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html


    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)


    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


if __name__ == '__main__':

    if not (len(sys.argv) == 3):
        print("Arguments: client_id and client_secret")
        sys.exit(1)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    server = OAuth2Server(*sys.argv[1:])
    server.browser_authorize()

    # test_response = server.oura.user_info()

    print('TOKEN\n=====\n')
    for key, value in server.oura.client.session.token.items():
        print('{} = {}'.format(key, value))
