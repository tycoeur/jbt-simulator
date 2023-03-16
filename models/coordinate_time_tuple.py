# -*- coding: utf-8 -*-
from typing import Final


class CoordinateTimeTuple(object):
    def __init__(self, coordinate: str, time: str):
        self.coordinate: Final[str] = coordinate
        self.time: Final[str] = time

    def __str__(self):
        return f"CoordinateTimeTuple[{self.coordinate}, {self.time}]"

    def __repr__(self):
        return f"({self.coordinate}, {self.time})"

    def print(self):
        print(str(self))
