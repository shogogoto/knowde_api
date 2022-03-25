import pytest

from fastapi.testclient import TestClient
from api import app
from fastapi import status

client = TestClient(app)


# body -> jsonキーワード引数
# form -> dataキーワード引数
def test_register_user():
    response = client.post(
        "/token",
        data={
            "username":  "test_id",
            "password": "password"
    })
    # response = client.get(
    #     "/users/")
    print(dir(status))
    print(response.json())
