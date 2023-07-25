from data import *
from dijkstra import calc_path
from path import *

path = calc_path(entry_point, exit_point)
# for seg in seg_path(path):
#     print(seg)

for cmd in path_to_commands(path):
    print(cmd, end='')