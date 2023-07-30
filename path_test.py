import data
from map import Direction
from path import path_to_commands
from dijkstra import calc_path

if __name__ == '__main__':
    target = data.current_map.state_of(8, 0, Direction.F)
    path = calc_path(data.entry_point, target)
    print(''.join([str(cmd) for cmd in path_to_commands(path)]))