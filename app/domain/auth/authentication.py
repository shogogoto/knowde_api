from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from domain import check_type
from .password import PlainPassword, HashedPassword, Password

def authorize_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detal,
        headers={"WWW-Authenticate": "Bearer"}
    )


class Expires:
    pass


class AccessToken:
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # create access token
    @classmethod
    def encode(cls, data: dict):
        to_encode = data.copy()
        # if expires_delta:
        #     expire = datetime.utcnow() + expires_delta
        # else:
        # expire = datetime.utcnow() + timedelta(minutes=15)
        # to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, cls.ALGORITHM)

    @classmethod
    def decode(cls, token: str):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        except JWTError:
            authorize_exception("Could not validate credentials")
        return payload


class OAuth2:
    def __init__(self, userRepository):
        self._scheme = OAuth2PasswordBearer(tokenUrl="token")

    def authenticateUser(self, userId: str, pasword: PlainPassword):
        pass

    def scheme(self):
        return self._scheme


class Credential:
    def __init__(self, userId: str, password: Password):
        self._userId    = check_type(userId, str)
        self._password  = check_type(password, Password)

    @property
    def userId(self) -> str:
        return self._userId

    def hash(self):
        return self._password.hash()

    def verify(self, password: str):
        check_type(password, str)
        return self._password.verify(password)



