from typing import List
from dataclasses import dataclass
from map import Path

@dataclass
class Command:
    name: str
    args: List[str]

    def __str__(self):
        s = self.name
        for arg in self.args:
            s += ' ' + arg
        s += ';'
        return s

def gen_cmd_straight_dis(mm: int) -> Command:
    return Command('f', [str(mm)])


def gen_cmd_straight_l(count: int) -> Command:
    return Command('l', [str(count)])

def gen_cmd_straight_r(count: int) -> Command:
    return Command('r', [str(count)])

def gen_cmd_backward_l(count: int) -> Command:
    return Command('bl', [str(count)])

def gen_cmd_backward_r(count: int) -> Command:
    return Command('br', [str(count)])

def gen_cmd_stop() -> Command:
    return Command('s', [])

def gen_cmd_turn_left(count = 1) -> Command:
    return Command('L', []) if count == 1 else Command('L', [str(count)])

def gen_cmd_turn_right(count = 1) -> Command:
    return Command('R', []) if count == 1 else Command('R', [str(count)])

def gen_cmd_backward_turn_left(count = 1) -> Command:
    return Command('bL', []) if count == 1 else Command('bL', [str(count)])

def gen_cmd_backward_turn_right(count = 1) -> Command:
    return Command('bR', []) if count == 1 else Command('bR', [str(count)])

