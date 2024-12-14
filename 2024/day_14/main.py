import re
from dataclasses import dataclass

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for second, line in enumerate(input):
        input[second] = line.replace("\n", "")

@dataclass
class vec2_t:
    x: int
    y: int

type pos_t = vec2_t
type vel_t = vec2_t

@dataclass
class Robot:
    pos: pos_t
    vel: vel_t

def construct_robots(input: list[str]) -> list[Robot]:
    robots: list[Robot] = []
    for line in input:
        # line is in format p=0,4 v=3,-3
        match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        if match:
            pos = vec2_t(int(match.group(1)), int(match.group(2)))
            vel = vec2_t(int(match.group(3)), int(match.group(4)))
            robots.append(Robot(pos=pos, vel=vel))
    return robots

robots: list[Robot] = construct_robots(input)

def move_robot(robot: Robot, room_size: vec2_t) -> Robot:
    return Robot(
        pos=vec2_t((robot.pos.x + robot.vel.x) % room_size.x, (robot.pos.y + robot.vel.y) % room_size.y),
        vel=robot.vel
    )

def multimove_robot(robot: Robot, room_size: vec2_t, steps: int) -> Robot:
    for _ in range(steps):
        robot = move_robot(robot, room_size)
    return robot

def print_floor(robots: list[Robot], room_size: vec2_t):
    """debug"""
    floor = [["." for _ in range(room_size.x)] for _ in range(room_size.y)]
    for robot in robots:
        cur_count: int = int(floor[robot.pos.y][robot.pos.x]) if floor[robot.pos.y][robot.pos.x] != "." else 0
        cur_count += 1
        floor[robot.pos.y][robot.pos.x] = str(cur_count)
    for row in floor:
        print("".join(row))

def move_robots_100_times(robots: list[Robot], room_size: vec2_t) -> list[Robot]:
    for i in range(100):
        robots = [move_robot(robot, room_size) for robot in robots]
    return robots

ROOM_SIZE: vec2_t = vec2_t(101, 103)

moved_robots: list[Robot] = move_robots_100_times(robots, ROOM_SIZE)

def safety_factor(robots: list[Robot], room_size: vec2_t) -> int:
    # q1 | q2
    # ---+---
    # q3 | q4
    q1: int = 0
    q2: int = 0
    q3: int = 0
    q4: int = 0
    for robot in robots:
        if robot.pos.x < room_size.x // 2 and robot.pos.y < room_size.y // 2:
            q1 += 1
        elif robot.pos.x > room_size.x // 2 and robot.pos.y < room_size.y // 2:
            q2 += 1
        elif robot.pos.x < room_size.x // 2 and robot.pos.y > room_size.y // 2:
            q3 += 1
        elif robot.pos.x > room_size.x // 2 and robot.pos.y > room_size.y // 2:
            q4 += 1
    return q1 * q2 * q3 * q4

safety: int = safety_factor(moved_robots, ROOM_SIZE)
print("Part 1:", safety)

# part 2
def check_christmas_tree_easter_egg(cnt) -> bool:
    possitions = set()
    for robot in robots:
        x = robot.pos.x
        y = robot.pos.y
        vx = robot.vel.x
        vy = robot.vel.y

        x += cnt * vx
        y += cnt * vy

        x = ((x % ROOM_SIZE.x) + ROOM_SIZE.x) % ROOM_SIZE.x
        y = ((y % ROOM_SIZE.y) + ROOM_SIZE.y) % ROOM_SIZE.y

        possitions.add((x, y))

    # I am too lazy to code this so I yoinked from (massive thanks):
    # https://github.com/AdamBalski/adventofcode/blob/main/14/solution2.py
    passed_test = False
    required_box_side = 3
    for i in range(ROOM_SIZE.x - required_box_side + 1):
        for j in range(ROOM_SIZE.y - required_box_side + 1):
            fails = False
            for required_x in range(i, i + required_box_side):
                for required_y in range(i, i + required_box_side):
                    if (required_x, required_y) not in possitions:
                        fails = True
                        break
                if fails:
                    break
            if not fails:
                passed_test = True
                break

        if passed_test:
            break

    return passed_test

for second in range(ROOM_SIZE.y * ROOM_SIZE.x):
    if second % 500 == 0:
        print(100 * second / (ROOM_SIZE.y * ROOM_SIZE.x), "%")
    if ok := check_christmas_tree_easter_egg(second):
        break

print("Part 2:", second)
