from oura import OuraOAuth2Client
import requests_mock
import json

def test_build_authorize_endpoint():
    client = OuraOAuth2Client("test_client", "test_secret")
    actual_url, state = client.authorize_endpoint(scope=["email", "daily"], state="foo")
    expected = "https://cloud.ouraring.com/oauth/authorize?response_type=code&client_id=test_client&scope=email+daily&state=foo"
    assert expected == actual_url
    assert "foo" == state

def test_token_request():
    client = OuraOAuth2Client("test_client", "test_secret")
    fake_code = "fake_code"
    with requests_mock.mock() as m:
        m.post(client.TOKEN_BASE_URL, text=json.dumps({
            'access_token': 'fake_return_access_token',
            'refresh_token': 'fake_return_refresh_token'
        }))
        retval = client.fetch_access_token(fake_code)
    assert "fake_return_access_token" == retval['access_token']
    assert "fake_return_refresh_token" == retval['refresh_token']
