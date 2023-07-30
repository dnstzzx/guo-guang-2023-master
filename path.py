from map import Car_State, Direction, Path
from command import *

@dataclass
class Path_Segment:
    states: List[Car_State]

    def __str__(self):
        return  str(self.states[0]) + ' -> ' + str(self.states[-1])
    
    @property
    def car_dir(self):
        return self.states[0].toward
    
    @property
    def move_dir(self):
        return self.car_dir.opposite if self.is_backward else self.car_dir
    
    @property
    def is_backward(self):
        return self.straight_length != 0 and \
            self.states[0].pos.get_neighbor_to(self.states[0].toward) != self.states[1].pos
    
    @property
    def straight_length(self):
        start, end = self.states[0], self.states[-1]
        if start.pos == end.pos:
            return 0
        elif start.pos.x == end.pos.x:
            return abs(start.pos.y - end.pos.y)
        elif start.pos.y == end.pos.y:
            return abs(start.pos.x - end.pos.x)

        return None

        


def seg_path(path: Path) -> List[Path_Segment]:
    segs:List[Path_Segment] = []
    current: List[Car_State] = [path.states[0]]
    for state in path.states[1:]:
        last = current[-1]
        pos, toward = state
        if toward != last.toward:
            segs.append(Path_Segment(current))
            current = []
        current.append(state)
    segs.append(Path_Segment(current))
    return segs

        

def path_to_commands(path: Path) -> List[Command]:
    cmds = []
    segs = seg_path(path)
    current = segs[0]
    for next in segs[1:]:
        # 生成本段直行
        dir = current.move_dir
        left_dir = dir.relative_apply(Direction.L)
        right_dir = left_dir.opposite

        left_line_count, right_line_count = 0, 0
        for pos, _ in current.states[1:]:
            if pos.has_neighbor_to(left_dir):
                left_line_count += 1
            if pos.has_neighbor_to(right_dir):
                right_line_count += 1

        if current.straight_length != 0:
            if left_line_count == 0 and right_line_count == 0:
                cmds.append(gen_cmd_straight_dis(400 * current.straight_length, current.is_backward))
            else:
                end_pos = current.states[-1].pos
                using_left = True if not end_pos.has_neighbor_to(right_dir) else \
                                False if not end_pos.has_neighbor_to(left_dir) else \
                                left_line_count > right_line_count
                cmds.append(gen_cmd_straight_branch(current.is_backward, 
                                                    Direction.L if using_left else Direction.R, 
                                                    left_line_count if using_left else right_line_count))

        # 生成衔接转弯
        if current.car_dir != next.car_dir:
            # using_back = next.is_backward
            car_turn = current.car_dir.relative_get(next.car_dir)
            using_back = not current.states[-1].pos.has_neighbor_to(next.car_dir)
            using_scanner_dir = current.car_dir.opposite if using_back else current.car_dir
            turning_dir = current.car_dir.relative_get(next.car_dir)
            if turning_dir == Direction.L:
                cmds.append(gen_cmd_turn_left(1, using_back))
            elif turning_dir == Direction.R:
                cmds.append(gen_cmd_turn_right(1, using_back))
            elif turning_dir == Direction.B:
                last_pos = current.states[-1].pos
                has_left = last_pos.has_neighbor_to(using_scanner_dir.relative_apply(Direction.L))
                #has_right = last_pos.has_neighbor_to(current.toward.relative_apply(Direction.L))
                cmds.append(gen_cmd_turn_left(1 + int(has_left), using_back))

        current = next
    
    if current.straight_length != 0:
        cmds.append(gen_cmd_straight_dis(400 * current.straight_length, current.is_backward))
    
    cmds.append(gen_cmd_stop())
    return cmds