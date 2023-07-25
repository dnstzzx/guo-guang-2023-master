from map import Car_State, Direction, Path
from command import *

@dataclass
class Path_Segment:
    states: List[Car_State]

    def __str__(self):
        return  str(self.states[0]) + ' -> ' + str(self.states[-1])
    
    @property
    def toward(self):
        return self.states[0].toward
    
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
    current: List[state] = [path.states[0]]
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
    count = 0
    for next in segs[1:]:
        count += 1
        dir = current.toward
        left_dir = dir.relative_apply(Direction.L)
        right_dir = left_dir.opposite
        left_line_count, right_line_count = 0, 0
        for pos, _ in current.states[1:]:
            if pos.has_neighbor_to(left_dir):
                left_line_count += 1
            if pos.has_neighbor_to(right_dir):
                right_line_count += 1
        print(left_line_count, right_line_count)


        turning_dir = current.toward.relative_get(next.toward)

        if left_line_count == 0 and right_line_count == 0:
            cmds.append(gen_cmd_straight_dis(400 * current.straight_length))
        else:
            cmds.append(gen_cmd_straight_l(left_line_count) if turning_dir == Direction.L else 
                        gen_cmd_straight_r(right_line_count))

        
        if turning_dir == Direction.L:
            cmds.append(gen_cmd_turn_left(1))
        elif turning_dir == Direction.R:
            cmds.append(gen_cmd_turn_right(1))

        current = next
    
    if current.straight_length == 0:
        turning_dir = current.toward.relative_get(next.toward)
        if turning_dir == Direction.L:
            cmds.append(gen_cmd_turn_left(1))
        elif turning_dir == Direction.R:
            cmds.append(gen_cmd_turn_right(1))
    else:
        cmds.append(gen_cmd_straight_dis(400 * current.straight_length))
    
    cmds.append(gen_cmd_stop())
    return cmds