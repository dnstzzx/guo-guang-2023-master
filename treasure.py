from typing import Dict, List, Tuple
from map import Car_State, Path
import dijkstra, dp
from vision import deep
from config import configs

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

    def update(self, recn_rst: deep.Treasure_Reco_Result):
        self.known = True
        if recn_rst.major_recognized:
            self.mine = (recn_rst.majar_is_red == configs.we_are_red)
            self.real = (recn_rst.minor_is_green == recn_rst.majar_is_red) if recn_rst.minor_recognized else True
            if not self.twin.known:
                twin_rst = deep.Treasure_Reco_Result(True, recn_rst.major_recognized, not recn_rst.majar_is_red, not recn_rst.minor_is_green)
                self.twin.update(twin_rst)

        else:
            self.mine = False
            self.real = False

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
    
    @property
    def reach_points(self) -> List[Car_State]:
        pos = self.pos
        pts = [Car_State(pos.get_neighbor_to(dir), dir) for dir in pos.get_neighbor_directions()]
        return pts
    
    @property
    def twin(self):
        return treasures_dict[(9 - self.pos.x, 9 - self.pos.y)]


treasures_dict: Dict[Tuple[int], Treasure] = {}

def get_interest_treasures():
    return [t for t in treasures_dict.values() if t.is_interest]

def determine_treasure_order(current: Car_State, end: Car_State) -> List[Treasure]:
    interest_treasures = get_interest_treasures()
    state_to_treasure = {Car_State(it.pos, it.pos.get_neighbor_directions()[0]): it for it in interest_treasures}
    cost_dict = dijkstra.calc_cost_dict(list(state_to_treasure.keys()) + [current, end])
    state_order = dp.calc_car_state_order(current, end, state_to_treasure.keys(), cost_dict)
    treasure_order = [state_to_treasure[s] for s in state_order]
    return treasure_order

def get_best_reach_point(current: Car_State, t: Treasure) -> Car_State:
    pts = t.reach_points
    if len(pts) == 1:
        return pts[0]

    lowest_cost = 9999
    best_reach_point = None
    for p in pts:
        path, cost = dijkstra.calc_path_and_cost(current, p)
        if cost < lowest_cost:
            lowest_cost, best_reach_point = cost, p
    return best_reach_point

# def calc_path_to_treasure(current: Car_State, t: Treasure):
#     pos = t.pos
#     lowest_cost = 9999
#     shortest_path = Path([])
#     for d in pos.get_neighbor_directions():
#         end = Car_State(pos.get_neighbor_to(d), d.opposite)
#         path, cost = dijkstra.calc_path_and_cost(current, end)
#         if cost < lowest_cost:
#             lowest_cost, shortest_path = cost, path
#     return shortest_path
