"""Person class that represents a person."""
from dataclasses import dataclass, field
from typing import List

from lib.utils import validate_email

#@dataclass
class Person:
    def __init__(self, first_name: str, last_name: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError('First name must be a string')
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if not isinstance(last_name, str):
            raise TypeError('Last name must be a string')
        self._last_name = last_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not isinstance(email, str):
            raise TypeError('Email must be a string')

        if not validate_email(email):
            raise TypeError('Email must be a valid email address')
        self._email = email

    def __str__(self) -> str:
        return f"{self._first_name} {self._last_name}"

@dataclass
class Traveller(Person):
    """Is a user that has traveller """

    favorite_country: str | None = None
    past_trips: list = field(default_factory=list)