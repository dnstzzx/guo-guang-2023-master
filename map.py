from dataclasses import dataclass
from enum import Enum
from typing import List, NamedTuple, Union

# 地图相关

# 地图坐标系: 原点为左下角,x轴正方向为右,y轴正方向为上
class Direction(Enum):
    F = 0
    R = 1 
    B = 2
    L = 3

    @property
    def map_border_mask(self):
        return 1 << self.value

    @property
    def coord_delta(self):
        _deltas = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]
        return _deltas[self.value]
    
    @property
    def x_delta(self):
        return self.coord_delta[0]

    @property
    def y_delta(self):
        return self.coord_delta[1]

    @property
    def opposite(self) -> 'Direction':
        return Direction((self.value + 2) % 4)
    
    def relative_apply(self, to: 'Direction') -> 'Direction':
        return Direction((self.value + to.value) % 4)
    
    def relative_get(self, to: 'Direction') -> 'Direction': # 计算到达目标方向的相对方向
        return Direction((to.value - self.value) % 4)
    

class Cell(NamedTuple):
    x: int
    y: int
    map: 'Map'

    def has_neighbor_to(self, dir: Direction) -> bool:
        return self.map.borders[self.x][self.y] & dir.map_border_mask == 0
            
    def get_neighbor_to(self, dir: Direction) -> Union['Cell', None]:
        return self.map.cells[self.x + dir.x_delta][self.y + dir.y_delta] if self.has_neighbor_to(dir) else None
    
    def get_neighbors(self):
        return [self.get_neighbor_to(dir) for dir in Direction if self.has_neighbor_to(dir)]

    def get_neighbor_directions(self) -> List[Direction]:
        return [dir for dir in Direction if self.has_neighbor_to(dir)]
    
    def is_nearby(self, other: 'Cell') -> bool:
        delta_x = abs(self.x - other.x)
        delta_y = abs(self.y - other.y)
        return (delta_x <= 1 and delta_y == 0) or (delta_y <= 1 and delta_x == 0)

    def get_direction_to(self, cell: 'Cell') -> Union[Direction, None]:
        dx = cell.x - self.x
        dy = cell.y - self.y

        if dx == 0 and dy == 1:
            return Direction.F
        elif dx == 1 and dy == 0:
            return Direction.R
        elif dx == 0 and dy == -1:
            return Direction.B
        elif dx == -1 and dy == 0:
            return Direction.L
        return None
    
    def set_border(self, dir: Direction, has_barrier: bool):
        if self.has_neighbor_to(dir):
            self.map._set_border(self.get_neighbor_to(dir), dir.opposite, has_barrier)  # type: ignore
        self.map._set_border(self, dir, has_barrier)


class Car_State(NamedTuple):
    pos: Cell
    toward: Direction
    
    def __str__(self):
        return f"({self.pos.x}, {self.pos.y}, {self.toward})"

@dataclass
class Path:
    states: List[Car_State]

    def check(self) -> bool:
        """检查路径的有效性"""
        if len(self.states) == 0:
            return False
        
        prev = self.states[0]
        for state in self.states[1:]:
            direction = prev.pos.get_direction_to(state.pos)
            if direction is None:
                return False
            if prev.toward != direction:
                return False
            prev = state
        return True

    def get_start(self) -> Car_State:
        """获取路径的起点"""
        return self.states[0]

    def get_end(self) -> Car_State:
        """获取路径的终点"""
        return self.states[-1]

    def __str__(self):
        return " -> ".join(str(s) for s in self.states)

# 地图坐标系: 原点为左下角,x轴正方向为右,y轴正方向为上
class Map:
    width: int
    height: int
    cells: List[List[Cell]] # [[col0],...]  cells[x][y]
    borders: List[List[int]]    # 坐标x, y的四周墙壁, 0-3位分别表示前右后左,1有墙壁0无
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = [[Cell(i, j, self) for j in range(height)] for i in range(width)]
        self.borders = [[0 for _ in range(height)] for _ in range(width)]

        # 为地图边界cell添加border
        for i in range(width):
            for j in range(height):
                cell = self.cells[i][j]
                if i == 0:
                    self._set_border(cell, Direction.L, True)
                if i == width-1:
                    self._set_border(cell, Direction.R, True)
                if j == 0:
                    self._set_border(cell, Direction.B, True)
                if j == height-1:
                    self._set_border(cell, Direction.F, True)

    def _set_border(self, cell: Cell, direction: Direction, has_barrier):
        if cell.map != self:
            print("wrong map while setting border!")
            return
        i, j = cell.x, cell.y
        if has_barrier:
            self.borders[i][j] |= direction.map_border_mask
        else:
            self.borders[i][j] &= ~direction.map_border_mask
    
    def cell_of(self, i, j) -> Cell:
        return self.cells[i][j]

    def state_of(self, i, j, toward):
        return Car_State(self.cell_of(i, j), toward)
            

@dataclass
class Treasure:
    pos: Cell
    known: bool
    mine: bool
    real: bool
    pushed: bool