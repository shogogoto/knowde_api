from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from passlib.context import CryptContext
from models import check_type

class Password(metaclass=ABCMeta):
    def __init__(self, value: str):
        self._value = check_type(value, str)
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def value(self):
        return self._value

    @abstractmethod
    def hash(self):
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str) -> bool:
        raise NotImplementedError


class HashedPassword(Password):
    def hash(self):
        return self

    def verify(self, plain_password: str) -> bool:
        check_type(plain_password, str)
        return self._context.verify(plain_password, self._value)


class PlainPassword(Password):
    def hash(self) -> HashedPassword:
        hashed = self._context.hash(self._value)
        return HashedPassword(hashed)

    def verify(self, hashed_password: str) -> bool:
        check_type(hashed_password, str)
        return self._context.verify(self._value, hashed_password)

