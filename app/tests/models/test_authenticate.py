import pytest
from models.auth import Credential, PlainPassword, HashedPassword

value  = "secret"
plain  = PlainPassword(value)
hashed = plain.hash()
userId = "test_id"

def test_by_plain():
    cred = Credential(userId, plain)
    assert cred.verify(hashed.value)

def test_by_hashed():
    cred = Credential(userId, hashed)
    assert cred.verify(plain.value)

# def test_token():
#     to_encode = {"sub": "username"} #, expires_delta=}
#     token   = auth.AccessToken.encode(to_encode)
#     payload = auth.AccessToken.decode(token)
#     token2  = auth.AccessToken.encode(payload)
#     assert token == token2
