# -*- coding: utf-8 -*-


class Note(object):
    def __init__(self, note: str, t: float, positions: list[int], bpm: float):
        self.note: str = note
        self.t: float = t
        self.positions: list[int] = positions
        self.bpm: float = bpm

    def to_string(self):
        return "Note[%s, %d, %s, %.4f]" % (self.note, int(self.t), self.positions, self.bpm)

    def print(self):
        print(self.to_string())
