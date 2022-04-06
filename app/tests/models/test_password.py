import pytest

from domain.auth import PlainPassword, HashedPassword


def test_verify():
    p1 = PlainPassword("secret")
    p2 = p1.hash()
    assert p1.verify(p2.value)
    assert p2.verify("secret")
