from ast import Set, Tuple
from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class Treasure_Map_Reco_Result:
    points: Set(Tuple(int))

    def check(self) -> Tuple[bool, str]:
        if len(self.points) != 8:
            return (False, f'宝藏个数为{len(self.points)}')
        for i, j in self.points:
            if i < 0 or i < 0 or i > 9 or j > 9:
                return (False, f'越界坐标:{i, j}')
            if (j, i) not in self.points:
                return (False, f'宝藏({i},{j})没有对称坐标')
        

class Treasure_Reco_Result(NamedTuple):
    major_recognized: bool 
    minor_recognized: bool
    majar_is_red: bool
    minor_is_green: bool



def recognize_treasure_map(img) -> Treasure_Map_Reco_Result:
    pass

def recognize_treasure(img) -> Treasure_Reco_Result:
    pass