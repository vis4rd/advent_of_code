from enum import StrEnum


class MapObject(StrEnum):
    EMPTY = "."
    WALL = "#"
    OOB = " "
    VISITED = "X"
    OBSTACLE = "O"

class HeroDirection(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

lab: list[str] = input

def print_lab(lab: list[str]) -> None:
    for row in lab:
        print(row)

HEIGHT: int = len(lab)
WIDTH: int = len(lab[0])

def find_hero(lab: list[str]) -> tuple[int, int]:
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if lab[i][j] in [HeroDirection.UP, HeroDirection.DOWN, HeroDirection.LEFT, HeroDirection.RIGHT]:
                return i, j
    return -1, -1

def get_hero_direction(lab: list[str], pos: tuple[int, int]) -> HeroDirection:
    i, j = pos
    return HeroDirection(lab[i][j])

HERO_POS: tuple[int, int] = find_hero(lab)
HERO_DIR: HeroDirection = get_hero_direction(lab, HERO_POS)

def next_pos() -> tuple[int, int]:
    i, j = HERO_POS
    next_pos = -1, -1
    match HERO_DIR:
        case HeroDirection.UP:
            next_pos = i - 1, j
        case HeroDirection.DOWN:
            next_pos = i + 1, j
        case HeroDirection.LEFT:
            next_pos = i, j - 1
        case HeroDirection.RIGHT:
            next_pos = i, j + 1
    return next_pos

def get_map_object_in_front(lab: list[str]) -> MapObject:
    pos_in_front: tuple[int, int] = next_pos()

    if pos_in_front[0] < 0 or pos_in_front[0] >= HEIGHT or pos_in_front[1] < 0 or pos_in_front[1] >= WIDTH:
        return MapObject.OOB

    return MapObject(lab[pos_in_front[0]][pos_in_front[1]])

def mark_tile_visited(lab: list[str]) -> None:
    i, j = HERO_POS
    lab[i] = lab[i][:j] + "X" + lab[i][j + 1:]

def mark_tile_as_hero(lab: list[str]) -> None:
    i, j = HERO_POS
    lab[i] = lab[i][:j] + HERO_DIR.value + lab[i][j + 1:]

def rotate_right(lab: list[str]) -> None:
    global HERO_DIR
    next_hero_dir: HeroDirection = HeroDirection.UP
    match HERO_DIR:
        case HeroDirection.UP:
            next_hero_dir = HeroDirection.RIGHT
        case HeroDirection.DOWN:
            next_hero_dir = HeroDirection.LEFT
        case HeroDirection.LEFT:
            next_hero_dir = HeroDirection.UP
        case HeroDirection.RIGHT:
            next_hero_dir = HeroDirection.DOWN
    HERO_DIR = next_hero_dir
    mark_tile_as_hero(lab)

def move_straight(lab: list[str]) -> None:
    global HERO_POS
    i, j = HERO_POS
    next_pos_ = next_pos()

    mark_tile_visited(lab)
    HERO_POS = next_pos_
    mark_tile_as_hero(lab)

def move(lab: list[str]) -> bool:
    match get_map_object_in_front(lab):
        case MapObject.WALL:
            rotate_right(lab)
        case MapObject.OBSTACLE:
            rotate_right(lab)
        case MapObject.EMPTY:
            move_straight(lab)
        case MapObject.VISITED:
            move_straight(lab)
        case MapObject.OOB:
            return False
    return True


def count_visited_tiles(lab: list[str]) -> int:
    count: int = 1
    for row in lab:
        count += row.count(MapObject.VISITED)
    return count

# part 1

go = True
lab_copy: list[str] = lab.copy()
while(go):
    go = move(lab_copy)
print("Part 1:")
print_lab(lab_copy)
print(HERO_POS)
print(f"Visited {count_visited_tiles(lab_copy)} tiles")
print()

# part 2

def reset_hero(lab: list[str]) -> None:
    global HERO_POS, HERO_DIR
    HERO_POS = find_hero(lab)
    HERO_DIR = get_hero_direction(lab, HERO_POS)

class HeroState:
    def __init__(self, pos: tuple[int, int], dir: HeroDirection):
        self.pos: tuple[int, int] = pos
        self.dir: HeroDirection = dir

reset_hero(lab)
hero_history: list[HeroState] = [HeroState(HERO_POS, HERO_DIR)]
obstacles_causing_loops: list[tuple[int, int]] = []

def mark_tile_as_obstacle(lab: list[str], pos: tuple[int, int]) -> None:
    i, j = pos
    if i < 0 or i >= HEIGHT or j < 0 or j >= WIDTH:
        return
    lab[i] = lab[i][:j] + "O" + lab[i][j + 1:]

def is_looped() -> bool:
    for hero_state in hero_history:
        if hero_state.pos == HERO_POS and hero_state.dir == HERO_DIR:
            return True
    return False

def find_loops() -> int:
    def construct_obstacle_candidate_list(lab: list[str]) -> list[tuple[int, int]]:
        go = True
        candidates: list[tuple[int, int]] = []
        while(go):
            candidates.append(next_pos())
            go = move(lab)
        return candidates

    def move_until_loop_detected_or_oob(lab: list[str]) -> bool:
        go: bool = True
        while(go):
            # print_lab(lab_copy)
            # print()
            if is_looped():
                return True
            hero_history.append(HeroState(HERO_POS, HERO_DIR))
            go = move(lab)
        return False

    i = 0
    obstacle_causing_loops_count: int = 0
    lab_copy: list[str] = lab.copy()
    candidates: list[tuple[int, int]] = construct_obstacle_candidate_list(lab_copy)
    for obstacle_pos in candidates:
        lab_copy = lab.copy()
        reset_hero(lab)
        hero_history.clear()
        print(f"Analyzing iteration {i}, obstacle candidate = {obstacle_pos}")
        i += 1
        if obstacle_pos not in obstacles_causing_loops:
            obstacles_causing_loops.append(obstacle_pos)
        else:
            continue

        reset_hero(lab)
        lab_copy = lab.copy()
        mark_tile_as_obstacle(lab_copy, obstacle_pos)
        # print_lab(lab_copy)
        # print()
        has_loop: bool = move_until_loop_detected_or_oob(lab_copy)
        if has_loop:
            obstacle_causing_loops_count += 1

    return obstacle_causing_loops_count

combinations: int = find_loops()
print(f"Part 2: combinations = {combinations}")
