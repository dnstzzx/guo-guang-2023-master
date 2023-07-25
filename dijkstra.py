from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappush, heappop
from map import Cell, Car_State, Map, Path, Direction
from typing import Dict, List, NamedTuple, Tuple

# Cell, Car_State, Direction等类定义

INFINITY = float('inf')

@dataclass(order=True)
class Record():
    cost: float
    state: Car_State = field(compare=False)


def calc_path(start: Car_State, end: Car_State) -> Path:
    open_set: List[Record] = [Record(0, start)]    # 尚未处理的状态集合,使用优先队列实现,按照距离排序。
    came_from: Dict[Car_State, Car_State] = {}              # 记录了最短路径中每个状态的前一个状态。came_from[s]表示状态s的前一个状态。
    g_score: Dict[Car_State, int] = defaultdict(lambda: INFINITY)   # 记录从起点到每个状态的当前最短距离。
    g_score[start] = 0 
    
    while open_set:
        record = heappop(open_set)
        insert_cost , current = record.cost, record.state

        if insert_cost > g_score[current]:
            continue
        
        if current == end:
            return reconstruct_path(came_from, current)
            
        for neighbor, cost in get_neighbors(current):
            if neighbor.pos == current.pos and neighbor.toward == current.toward:
                continue
            tent_g_score = g_score[current] + cost
            
            if tent_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tent_g_score
                heappush(open_set, Record(tent_g_score, neighbor))
                
    return None # No path found

def reconstruct_path(came_from: dict, current: Car_State) -> Path:
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    path.reverse()
    return Path(path)

# 状态转移函数
def get_neighbors(state: Car_State) -> List[Tuple[Car_State, int]]:
    turn_cost = 1
    straight_cost = 1

    res:List[Tuple[Car_State, int]] = []
    pos, toward = state
    if pos.has_neighbor_to(toward):
        new_state = Car_State(pos.get_neighbor_to(toward), toward)
        cost = 1
        res.append((new_state, cost))
    for neib_dir in pos.get_neighbor_directions():
        if neib_dir == toward:
            continue
        new_state = Car_State(pos, neib_dir)
        cost = 1
        res.append((new_state, cost))
    return res

