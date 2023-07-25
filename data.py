from map import Cell, Direction, Car_State, Map


def build_origin_map() -> Map:
    # [[row0],...] True 有障碍,False 无障碍
    down_data = [[True, True, True, True, True, True, True, True, True, True], [True, False, False, True, False, False, False, True, False, False], [False, True, False, False, True, False, True, False, True, False], [True, False, True, False, True, True, False, False, False, True], [False, True, False, True, True, True, False, False, True, False], [False, True, True, False, True, True, False, True, True, False], [False, True, False, False, True, True, True, False, True, False], [True, False, False, False, True, True, False, True, False, True], [False, True, False, True, False, True, False, False, True, False], [False, False, True, False, False, False, True, False, False, True]]
    right_data = [[False, True, False, False, True, False, False, False, False, True], [False, True, True, False, False, True, False, True, True, True], [False, True, True, False, False, True, False, False, True, True], [True, False, False, True, False, False, True, True, False, True], [False, False, False, False, False, False, True, False, True, True], [True, False, True, False, False, False, False, False, False, True], [False, True, True, False, False, True, False, False, True, True], [True, False, False, True, False, False, True, True, False, True], [True, True, False, True, False, False, True, True, False, True], [False, False, False, False, True, False, False, True, False, True]]
    m = Map(10, 10)
    for i in range(10):
        for j in range(10):
            c = m.cells[i][j]
            c.set_border(Direction.R, right_data[j][i])
            c.set_border(Direction.B, down_data[j][i])
    return m

current_map = build_origin_map()

entry_point = current_map.state_of(0, 0, Direction.R)
exit_point = current_map.state_of(9, 9, Direction.R)
