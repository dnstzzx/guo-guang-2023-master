import dataclasses

from map import Cell


@dataclasses
class Treasure:
    pos: Cell
    known: bool
    mine: bool
    real: bool
    pushed: bool