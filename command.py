from turtle import back
from typing import List
from dataclasses import dataclass
from map import Direction, Path

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
    
def gen_cmd_enter() -> Command:
    return Command('ent', [])
    
def gen_cmd_stop() -> Command:
    return Command('s', [])

def gen_cmd_straight_dis(mm: int, backward: bool) -> Command:
    return Command('f' if not backward else 'bf', [str(mm)])

def gen_cmd_straight_l(count: int, backward= False):
    return Command('l' if not backward else 'bl', [str(count)])

def gen_cmd_straight_r(count: int, backward= False):
    return Command('r' if not backward else 'br', [str(count)])

def gen_cmd_turn_left(count: int, backward: bool = False):
    return Command('L' if not backward else 'bL', [] if count == 1 else [str(count)])

def gen_cmd_turn_right(count: int, backward: bool = False):
    return Command('R' if not backward else 'bR', [] if count == 1 else [str(count)])


def gen_cmd_straight_branch(backward: bool ,logical_branch_dir: Direction, branch_count: int):
    if logical_branch_dir == Direction.L:
        return gen_cmd_straight_l(branch_count, backward)
    elif logical_branch_dir == Direction.R:
        return gen_cmd_straight_r(branch_count, backward)