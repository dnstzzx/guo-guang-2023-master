from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappush, heappop
from itertools import permutations
from math import inf
from map import Cell, Car_State, Path, Direction
from typing import Dict, List, NamedTuple, Tuple, Union

class DP_State(NamedTuple):
    visited: int
    pos: int

def visited_1_idxs(visited: int):
    idxs = []
    i = 0
    while(visited != 0):
        if visited & 1 == 1:
            idxs.append(i)
        i += 1


def gen_visited_lines(node_count):
    visited_lines: List[List[int]] = [[] for _ in range(node_count)]
    def count1(num):
        return bin(num).count('1')

    for i in range(1 << node_count):
        visited_lines[count1(i) - 1].append(i)
    return visited_lines

# param costs: 邻接矩阵,0和1分别为起点和终点，其他为中间节点
# def calc_node_order(node_count, costs: List[List[float]]) -> List[int]:
#     from_start_costs = costs[0][2:]
#     to_end_costs = [costs[i + 2][1] for i in range(node_count)]
#     costs = [l[2:] for l in costs[2:]]

#     state_costs = [[-1 for _ in range(node_count)] for _ in range(1<<node_count)] # cost = state_costs[visited][last]
#     state_costs[0] = [0 for _ in range(node_count)]

#     for visited_line in gen_visited_lines(node_count):
#         for visited in visited_line:
#             for pos in range(node_count):
#                 if visited & 1 << pos == 0:
#                     continue
#                 last_visited = visited & (~(1 << pos))
#                 for last_pos in range(node_count):
#                     if last_visited & 1 << pos == 0:
#                         continue
#                     cost = state_costs[last_visited][last_pos] + \
#                             costs[last_pos][pos] if last_visited != 0 else from_start_costs[pos]


def calc_car_state_order(start: Car_State, end: Car_State, nodes: Car_State, cost_dict: Dict[Car_State, Dict[Car_State, float]]) -> List[Car_State]:
    best_cost = inf
    best = []

    for path in permutations(nodes):
        cost = cost_dict[start][path[0]]
        last = path[0]
        for node in path[1:]:
            cost += cost_dict[last][node]
            last = node
        cost += cost_dict[last][end]
        
        if cost < best_cost:
            best_cost, best = cost, path
    return best