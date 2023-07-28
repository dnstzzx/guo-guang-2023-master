from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappush, heappop
from map import Cell, Car_State, Path, Direction
from typing import Dict, List, NamedTuple, Tuple, Union

# Cell, Car_State, Direction等类定义

INFINITY = float('inf')

@dataclass(order=True)
class Record():
    cost: float
    state: Car_State = field(compare=False)


def calc_path_and_cost(start: Car_State, end: Car_State) -> Tuple[Path, float]:
    open_set: List[Record] = [Record(0, start)]    # 尚未处理的状态集合
    came_from: Dict[Car_State, Car_State] = {}              # 记录了最短路径中每个状态的前一个状态。came_from[s]表示状态s的前一个状态。
    g_score: Dict[Car_State, float] = defaultdict(lambda: INFINITY)   # 记录从起点到每个状态的当前最短距离。
    g_score[start] = 0 
    
    while open_set:
        record = heappop(open_set)
        insert_cost , current = record.cost, record.state

        if insert_cost > g_score[current]:
            continue
        
        if current == end:
            return (reconstruct_path(came_from, current), g_score[current])
            
        for neighbor, cost in get_neighbors(current):
            if neighbor.pos == current.pos and neighbor.toward == current.toward:
                continue
            tent_g_score = g_score[current] + cost
            
            if tent_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tent_g_score
                heappush(open_set, Record(tent_g_score, neighbor))
                
    return (None, INFINITY) # No path found


def calc_path(start: Car_State, end: Car_State) -> Union[Path, None]:
    return calc_path_and_cost(start, end)[0]

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
    if pos.has_neighbor_to(toward): # 向前
        new_state = Car_State(pos.get_neighbor_to(toward), toward) # type: ignore
        cost = 1
        res.append((new_state, cost))
    if pos.has_neighbor_to(toward.opposite): # 向后
        new_state = Car_State(pos.get_neighbor_to(toward.opposite), toward) # type: ignore
        cost = 1
        res.append((new_state, cost))
    for neib_dir in pos.get_neighbor_directions():  # 转弯
        if neib_dir == toward:
            continue
        new_state = Car_State(pos, neib_dir)
        cost = 1
        res.append((new_state, cost))
    return res


def calc_multi_cost(start: Car_State, ends: List[Car_State]) -> Dict[Car_State, float]:
    end_costs = {e: INFINITY for e in ends}
    rest_ends = set(ends)
    open_set: List[Record] = [Record(0, start)]    # 尚未处理的状态集合。
    g_score: Dict[Car_State, float] = defaultdict(lambda: INFINITY)   # 记录从起点到每个状态的当前最短距离。
    g_score[start] = 0 
    
    while open_set and rest_ends:
        record = heappop(open_set)
        insert_cost , current = record.cost, record.state

        if insert_cost > g_score[current]:
            continue
        
        if current in rest_ends:
            end_costs[current] = insert_cost
            rest_ends.remove(current)
            
        for neighbor, cost in get_neighbors(current):
            if neighbor.pos == current.pos and neighbor.toward == current.toward:
                continue
            tent_g_score = g_score[current] + cost
            
            if tent_g_score < g_score[neighbor]:
                g_score[neighbor] = tent_g_score
                heappush(open_set, Record(tent_g_score, neighbor))
    return end_costs


# 计算任意给定状态中任意两个之间的代价，假定路径可逆，返回一个对称邻接矩阵
def calc_cost_matrix(nodes: List[Car_State]):
    l = len(nodes)
    matrix = [[0.0 for _ in range(l)] for _ in range(l)]
    for i in range(l):
        costs = calc_multi_cost(nodes[i], nodes[i + 1:])
        for j in range(i+1, l):
            matrix[i][j] = matrix[j][i] = costs[nodes[j]]
    return matrix

# 计算任意给定状态中任意两个之间的代价，假定路径可逆，返回一个以Dict呈现的对称邻接矩阵
def calc_cost_dict(nodes: List[Car_State]) -> Dict[Car_State, Dict[Car_State, float]]:
    l = len(nodes)
    matrix = {node:{node:0.0 for node in nodes} for node in nodes}
    for i in range(l):
        start = nodes[i]
        costs = calc_multi_cost(start, nodes[i + 1:])
        for end, cost in costs.items():
            matrix[start][end] = matrix[end][start] = cost
    return matrix
