import pytest
from oura import OuraClient
import requests_mock
from requests_mock import ANY
import requests
from urllib.parse import urlparse, parse_qs
import json
import functools

adapter = requests_mock.Adapter()

def test_summary_url():
    client = OuraClient('test_id')
    url = client._build_summary_url(start='start-date', end=None, datatype='sleep')
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    assert 'end' not in params.keys()

    url2 = client._build_summary_url(start='start-date', end='end_date', datatype='sleep')
    parsed_url = urlparse(url2)
    params = parse_qs(parsed_url.query)
    assert 'end' in params.keys()


def test_token_refresh():
    update_called = []

    # hacky way to test side effect
    def token_updater(token):
        update_called.append(1)

    client = OuraClient('test_id', access_token='token', refresh_callback=token_updater)
    adapter.register_uri(requests_mock.POST, requests_mock.ANY, status_code=401, text=json.dumps({
            'access_token': 'fake_return_access_token',
            'refresh_token': 'fake_return_refresh_token'
        }))
    adapter.register_uri(requests_mock.GET, requests_mock.ANY, status_code=401, text=json.dumps({ 'a': 'b'}))

    client._session.mount(client.API_ENDPOINT, adapter)
    try:
        resp = client.user_info()
    except:
        pass
    assert len(update_called) == 1