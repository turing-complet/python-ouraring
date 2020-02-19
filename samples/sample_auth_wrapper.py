from oura import AuthenticationWrapper

"""
reference: https://cloud.ouraring.com/docs/
"""

client_id='client id of the oura application'
client_secret='client secret of the oura application'

auth_wrapper = AuthenticationWrapper(client_id, client_secret)
auth_wrapper.browser_authorize()

acc_t = auth_wrapper.oura_client.session.token['access_token']
ref_t = auth_wrapper.oura_client.session.token['refresh_token']