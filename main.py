from os import path
from numpy import Inf
from data import *
from dijkstra import *
from path import *


# 起点到终点最短路径
# path = calc_path(entry_point, exit_point)
# for seg in seg_path(path):
#     print(seg)

# # for cmd in path_to_commands(path):
# #     print(cmd, end='')

# exit()



# 纯贪心法,每次找最近点

# points = [(0, 7), (7, 7), (5, 6), (1, 5), (8, 4), (4, 3), (2, 2), (9, 2)]
# points = [current_map.cell_of(i, j) for i, j in points]
# states = []
# states = [Car_State(p.get_neighbor_to(p.get_neighbor_directions()[0]), p.get_neighbor_directions()[0].opposite) for p in points] # type: ignore


# costs = calc_cost_dict([entry_point, exit_point] + states)
# unvisited_states = set(states)
# current = entry_point
# cmds = []

# while unvisited_states:
#     nearest = (None, Inf)
#     for s in unvisited_states:
#         cost = costs[current][s]
#         if cost < nearest[1]:
#             nearest = (s, cost)

#     s = nearest[0]
#     path = calc_path(current, s)
#     # for seg in seg_path(path):
#     #     print(seg)
#     cmd = ''.join([str(c) for c in path_to_commands(path)])
#     cmds.append(cmd)
#     unvisited_states.remove(s)
#     current = s



# 到所有点位的全局最短路径

points = [(0, 7), (7, 7), (5, 6), (1, 5), (8, 4), (4, 3), (2, 2), (9, 2)]
points = [current_map.cell_of(i, j) for i, j in points]
states = []
states = [Car_State(p.get_neighbor_to(p.get_neighbor_directions()[0]), p.get_neighbor_directions()[0].opposite) for p in points] # type: ignore

costs = calc_cost_dict([entry_point, exit_point] + states)
from dp import calc_car_state_order
ordered_states = calc_car_state_order(entry_point, exit_point, states, costs)
paths = []
last = entry_point
for state in ordered_states:
    paths.append(calc_path(last, state))
    last = state
paths.append(calc_path(last, exit_point))
cmds = [''.join([str(c) for c in path_to_commands(path)]) for path in paths]

print(''.join(cmds))
