import dataclasses
from typing import Dict, List, Tuple
from map import Car_State, Path
import dijkstra, dp

from map import Cell

class Treasure:
    pos: Cell
    known: bool
    mine: bool
    real: bool
    pushed: bool

    def __init__(self, pos: Cell) -> None:
        self.pos = pos
        self.known = False
        self.mine = False
        self.real = False
        self.pushed = False

    @property
    def is_interest(self):
        if not self.known:
            return True
        if self.pushed:
            return False
        if self.mine and self.real:
            return True
        return False
    
    @property
    def is_hate(self):
        if not self.known:
            return True
        if self.mine and not self.real: # 我方伪宝藏
            return True
        if self.real and not self.mine: # 对方真宝藏
            return True
        return False

treasures: Dict[Tuple[int], Treasure] = {}


def determine_treasure_order(current: Car_State, end: Car_State) -> List[Treasure]:
    interest_treasures = [t for t in treasures.values() if t.is_interest]
    state_to_treasure = {Car_State(it.pos, it.pos.get_neighbor_directions[0]): it for it in interest_treasures}
    cost_dict = dijkstra.calc_cost_dict(state_to_treasure.keys())
    state_order = dp.calc_car_state_order(current, end, state_to_treasure.keys(), cost_dict)
    treasure_order = [state_to_treasure[s] for s in state_order]
    return treasure_order

def calc_path_to_treasure(current: Car_State, t: Treasure):
    pos = t.pos
    lowest_cost = 9999
    shortest_path = Path([])
    for d in pos.get_neighbor_directions():
        end = Car_State(pos.get_neighbor_to(d), d.opposite)
        path, cost = dijkstra.calc_path_and_cost(current, end)
        if cost < lowest_cost:
            lowest_cost, shortest_path = cost, path
    return shortest_path
