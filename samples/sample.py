import json
import os
from datetime import datetime

from oura import OuraClient


def get_self():
    pat = os.getenv("OURA_PAT")
    client = OuraClient(personal_access_token=pat)
    user_info = client.user_info()
    print(user_info)


def setEnvironment(envFile):
    basePath = os.path.dirname(os.path.abspath(__file__))
    fullPath = os.path.join(basePath, envFile)
    with open(fullPath) as file:
        env = json.load(file)
        os.environ["OURA_CLIENT_ID"] = env["client_id"]
        os.environ["OURA_CLIENT_SECRET"] = env["client_secret"]
        os.environ["OURA_ACCESS_TOKEN"] = env["access_token"]
        os.environ["OURA_REFRESH_TOKEN"] = env["refresh_token"]


def appendFile(filename, token_dict):

    basePath = os.path.dirname(os.path.abspath(__file__))
    fullPath = os.path.join(basePath, filename)
    with open(fullPath, "r+") as file:
        prev = json.load(file)
        curr = {
            "client_id": prev.pop("client_id"),
            "client_secret": prev.pop("client_secret"),
            "access_token": token_dict["access_token"],
            "refresh_token": token_dict["refresh_token"],
            "previous": json.dumps(prev),
        }
        file.seek(0)
        json.dump(curr, file)


def getOuraClient(envFile):
    client_id = os.getenv("OURA_CLIENT_ID")
    client_secret = os.getenv("OURA_CLIENT_SECRET")
    access_token = os.getenv("OURA_ACCESS_TOKEN")
    refresh_token = os.getenv("OURA_REFRESH_TOKEN")
    refresh_callback = lambda x: appendFile(envFile, x)

    auth_client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_callback=refresh_callback,
    )

    return auth_client


if __name__ == "__main__":

    envFile = "token.json"
    setEnvironment(envFile)
    client = getOuraClient(envFile)
    today = datetime.today()
    sleep = client.sleep_summary(today)
    print(sleep)
