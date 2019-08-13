from oura import OuraClient
import os
import json

def setEnvironment(envFile):
    with open(envFile) as file:
        env = json.load(file)
        os.environ['OURA_CLIENT_ID'] = env['client_id']
        os.environ['OURA_CLIENT_SECRET'] = env['client_secret']
        os.environ['OURA_ACCESS_TOKEN'] = env['access_token']
        os.environ['OURA_REFRESH_TOKEN'] = env['refresh_token']


def appendFile(filename, token_dict):
    if type(token_dict) is not dict:
        raise TypeError("Please supply a dict for the refresh callback, received type={0}".format(type(token_dict)))

    with open(filename, 'a') as file:
        prev = json.load(file)
        curr = {
            'client_id': prev.pop('client_id'),
            'client_secret': prev.pop('client_secret'),
            'access_token': token_dict['token_dict'],
            'refresh_token': token_dict['refresh_token'],
            'previous': json.dumps(prev)
        }
        json.dump(curr, file)


def getOuraClient():
    client_id = os.getenv('OURA_CLIENT_ID')
    client_secret = os.getenv('OURA_CLIENT_SECRET')
    access_token = os.getenv('OURA_ACCESS_TOKEN')
    refresh_token = os.getenv('OURA_REFRESH_TOKEN')
    refresh_callback = lambda x: appendFile('token.json', x)

    auth_client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_callback=refresh_callback
        )
    
    return auth_client

if __name__ == "__main__":
    
    setEnvironment('token.json')
    client = getOuraClient()
    sleep = client.sleep_summary()
    print(sleep)
