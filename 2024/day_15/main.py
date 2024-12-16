from dataclasses import dataclass
from enum import StrEnum

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for second, line in enumerate(input):
        input[second] = line.replace("\n", "")

input_warehouse: list[str] = input[: input.index("")]
input_moves: str = "".join(input[input.index("") + 1 :])

warehouse: list[str] = input_warehouse.copy()

@dataclass
class vec2:
    x: int
    y: int

WIDTH: int = len(warehouse[0])
HEIGHT: int = len(warehouse)

class RobotDir(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


DIRS: dict[RobotDir, vec2] = {
    RobotDir.LEFT: vec2(-1, 0),
    RobotDir.RIGHT: vec2(1, 0),
    RobotDir.UP: vec2(0, -1),
    RobotDir.DOWN: vec2(0, 1),
}


def find_robot(warehouse: list[str]) -> vec2:
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if warehouse[i][j] == "@":
                return vec2(j, i)
    return vec2(-1, -1)

def can_move(warehouse: list[str], pos: vec2, dir: vec2) -> bool:
    new_pos = vec2(pos.x + dir.x, pos.y + dir.y)
    if warehouse[new_pos.y][new_pos.x] == "#":
        return False
    elif warehouse[new_pos.y][new_pos.x] == "O":
        return can_move(warehouse, new_pos, dir)
    else:
        return True

def move(warehouse: list[str], pos: vec2, dir: vec2) -> None:
    new_pos = vec2(pos.x + dir.x, pos.y + dir.y)
    if warehouse[new_pos.y][new_pos.x] == "#":
        return
    elif warehouse[new_pos.y][new_pos.x] == "O":
        move(warehouse, new_pos, dir)
        if warehouse[new_pos.y][new_pos.x] == "O":
            return

    cur: str = warehouse[pos.y][pos.x]
    warehouse[pos.y] = warehouse[pos.y][: pos.x] + "." + warehouse[pos.y][pos.x + 1 :]
    warehouse[new_pos.y] = warehouse[new_pos.y][: new_pos.x] + cur + warehouse[new_pos.y][new_pos.x + 1 :]

def print_warehouse(warehouse: list[str]) -> None:
    """debug"""
    for row in warehouse:
        print(row)

def move_robot(warehouse: list[str], robot_pos: vec2, moves: str) -> None:
    for move_ in moves:
        if can_move(warehouse, robot_pos, DIRS[RobotDir(move_)]):
            move(warehouse, robot_pos, DIRS[RobotDir(move_)])
            robot_pos = vec2(robot_pos.x + DIRS[RobotDir(move_)].x, robot_pos.y + DIRS[RobotDir(move_)].y)

robot_init_pos: vec2 = find_robot(warehouse)
move_robot(warehouse, robot_init_pos, input_moves)

def boxes_gps(warehouse: list[str]) -> list[vec2]:
    boxes: list[vec2] = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if warehouse[i][j] == "O":
                boxes.append(vec2(j, i))
    return boxes

def sum_gps(gps: list[vec2]) -> int:
    return sum([gps_.y * 100 + gps_.x for gps_ in gps])

print("Part 1:", sum_gps(boxes_gps(warehouse)))

# part 2

def widen_warehouse(warehouse: list[str]) -> list[str]:
    new_warehouse: list[str] = [""] * len(warehouse)
    for i, row in enumerate(warehouse):
        for el in row:
            if el == "@":
                new_warehouse[i] += "@."
            elif el == ".":
                new_warehouse[i] += ".."
            elif el == "#":
                new_warehouse[i] += "##"
            elif el == "O":
                new_warehouse[i] += "[]"
    return new_warehouse

wide_warehouse = widen_warehouse(input_warehouse)

def can_move_wide(warehouse: list[str], pos: vec2, dir: vec2) -> bool:
    new_pos = vec2(pos.x + dir.x, pos.y + dir.y)
    if warehouse[new_pos.y][new_pos.x] == "#":
        return False
    elif warehouse[new_pos.y][new_pos.x] == "[":
        if dir == DIRS[RobotDir.UP] or dir == DIRS[RobotDir.DOWN]:
            return can_move_wide(warehouse, new_pos, dir) and can_move_wide(warehouse, vec2(new_pos.x + 1, new_pos.y), dir)
        else:
            return can_move_wide(warehouse, new_pos, dir)
    elif warehouse[new_pos.y][new_pos.x] == "]":
        if dir == DIRS[RobotDir.UP] or dir == DIRS[RobotDir.DOWN]:
            return can_move_wide(warehouse, new_pos, dir) and can_move_wide(warehouse, vec2(new_pos.x - 1, new_pos.y), dir)
        else:
            return can_move_wide(warehouse, new_pos, dir)
    else:
        return True

def move_wide(warehouse: list[str], pos: vec2, dir: vec2) -> None:
    new_pos = vec2(pos.x + dir.x, pos.y + dir.y)
    if warehouse[new_pos.y][new_pos.x] == "#":
        return
    elif warehouse[new_pos.y][new_pos.x] == "[":
        move_wide(warehouse, new_pos, dir)
        if dir == DIRS[RobotDir.UP] or dir == DIRS[RobotDir.DOWN]:
            move_wide(warehouse, vec2(new_pos.x + 1, new_pos.y), dir)

        if warehouse[new_pos.y][new_pos.x] == "[":
            return
    elif warehouse[new_pos.y][new_pos.x] == "]":
        move_wide(warehouse, new_pos, dir)
        if dir == DIRS[RobotDir.UP] or dir == DIRS[RobotDir.DOWN]:
            move_wide(warehouse, vec2(new_pos.x - 1, new_pos.y), dir)

        if warehouse[new_pos.y][new_pos.x] == "]":
            return

    cur: str = warehouse[pos.y][pos.x]
    warehouse[pos.y] = warehouse[pos.y][: pos.x] + "." + warehouse[pos.y][pos.x + 1 :]
    warehouse[new_pos.y] = warehouse[new_pos.y][: new_pos.x] + cur + warehouse[new_pos.y][new_pos.x + 1 :]

def move_robot_wide(warehouse: list[str], robot_pos: vec2, moves: str) -> None:
    for move_ in moves:
        if can_move_wide(warehouse, robot_pos, DIRS[RobotDir(move_)]):
            move_wide(warehouse, robot_pos, DIRS[RobotDir(move_)])
            robot_pos = vec2(robot_pos.x + DIRS[RobotDir(move_)].x, robot_pos.y + DIRS[RobotDir(move_)].y)

robot_init_widepos: vec2 = find_robot(wide_warehouse)
move_robot_wide(wide_warehouse, robot_init_widepos, input_moves)


def boxes_gps_wide(warehouse: list[str]) -> list[vec2]:
    boxes: list[vec2] = []
    for i in range(HEIGHT):
        for j in range(WIDTH*2):
            if warehouse[i][j] == "[":
                boxes.append(vec2(j, i))
    return boxes

print("Part 2:", sum_gps(boxes_gps_wide(wide_warehouse)))
