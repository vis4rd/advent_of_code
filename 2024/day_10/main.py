from enum import Enum

with open("2024/day_10/input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

type map_t = list[list[int]]
type loc_t = tuple[int, int]

map: map_t = []
for line in input:
    map.append([int(num) for num in line])


class Leaf[T]:
    def __init__(self, value: T):
        self.value: T = value
        self.children: list[Leaf[T]] = []

class Tree[T]:
    def __init__(self, root: Leaf[T]):
        self.root: Leaf[T] = root

    def calc_score(self) -> int:
        bottom_leaves: set[loc_t] = set()
        def count_leaves(leaf: Leaf[T]) -> None:
            nonlocal bottom_leaves
            if leaf.value.height == 9:
                bottom_leaves.add(leaf.value.pos)
            for child in leaf.children:
                count_leaves(child)
        count_leaves(self.root)
        return len(bottom_leaves)

    def calc_rating(self) -> int:
        sum_: int = 0
        def count_leaves(leaf: Leaf[T]) -> None:
            nonlocal sum_
            if leaf.value.height == 9:
                sum_ += 1
            for child in leaf.children:
                count_leaves(child)
        count_leaves(self.root)
        return sum_


def find_trailheads(map: map_t):
    trailheads: list[loc_t] = []
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == 0:
                trailheads.append((i, j))
    return trailheads

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

DIRECTIONS: list[Direction] = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

class Location:
    def __init__(self, x: int, y: int, height: int):
        self.pos: loc_t = (x, y)
        self.height = height

def construct_trees(trailheads: list[loc_t], map: map_t) -> list[Tree[Location]]:
    trees: list[Tree[Location]] = []
    for t_x, t_y in trailheads:
        loc: Location = Location(t_x, t_y, map[t_x][t_y])
        root: Leaf[Location] = Leaf(loc)
        trees.append(Tree(root))

    return trees

def find_next_step(map: map_t, pos: Leaf[Location]) -> None:
    for direction in DIRECTIONS:
        x, y = pos.value.pos
        try:
            next_x = x + direction.value[0]
            next_y = y + direction.value[1]
            if next_x < 0 or next_y < 0:
                continue
            map[next_x][next_y]
        except:
            continue
        else:
            if map[next_x][next_y] == (pos.value.height + 1):
                loc: Location = Location(next_x, next_y, map[next_x][next_y])
                pos.children.append(Leaf(loc))

def find_full_trail(map: map_t, tree: Tree[Location]) -> None:
    def find_leaf_trail(map: map_t, leaf: Leaf[Location]) -> None:
        find_next_step(map, leaf)
        for child in leaf.children:
            find_leaf_trail(map, child)

    find_leaf_trail(map, tree.root)

def find_trails(map: map_t) -> None:
    trailheads: list[loc_t] = find_trailheads(map)
    trees: list[Tree[Location]] = construct_trees(trailheads, map)

    for tree in trees:
        find_full_trail(map, tree)
    return trees

trail_trees: list[Tree[Location]] = find_trails(map)

print("Part 1:", sum(tree.calc_score() for tree in trail_trees))
print("Part 2:", sum(tree.calc_rating() for tree in trail_trees))
