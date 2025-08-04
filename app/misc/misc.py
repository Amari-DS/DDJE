import tkinter as tk
from enum import Enum
from functools import cached_property
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models import Root


class BindedEnum(Enum):

    def __new__(cls, value: Any, binded_value: Any) -> 'BindedEnum':
        obj = object.__new__(cls)
        obj._value_ = value
        obj.binded_value = binded_value
        return obj

    def __str__(self):
        return self.binded_value


class Storage(object):
    current_data: 'Root'


class NoteImage(object):

    def __init__(self, path: str, label: str) -> None:
        self.__path = path
        self.__label = label

    @cached_property
    def image(self):
        return tk.PhotoImage(file=self.__path)

    @property
    def label(self):
        return self.__label
