from helper import OuraModel, from_json


class UserInfo(OuraModel):
    _KEYS = ["age", "weight", "gender", "email"]


if __name__ == "__main__":

    test = """
{
    "age": 27,
    "weight": 80,
    "email": "john.doe@the.domain",
    "surprise" : "wow this is new"
}"""

    u = from_json(test, UserInfo)
    print(u)
