import itertools

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

type position = tuple[int, int]

antennas: dict[str, set[position]] = {}
HEIGHT: int = len(input)
WIDTH: int = len(input[0])

def register_antenna_type(name: str) -> None:
    if name not in antennas:
        antennas[name] = set()

def add_antenna(name: str, position: position) -> None:
    antennas[name].add(position)

def parse_input() -> None:
    for i, line in enumerate(input):
        for j, name in enumerate(line):
            if name != ".":
                register_antenna_type(name)
                add_antenna(name, (j, i))

parse_input()
# print(antennas)

def calc_antinode_pos(pos1: position, pos2: position) -> list[position]:
    diff: position = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    antinode1: position = (pos1[0] - diff[0], pos1[1] - diff[1])
    antinode2: position = (pos2[0] + diff[0], pos2[1] + diff[1])
    return [antinode1, antinode2]

def find_antinodes() -> set[position]:
    antinodes: set[position] = set()
    for antenna_type, positions in antennas.items():
        pairs = itertools.combinations(positions, 2)
        for pair in pairs:
            antinodes_= calc_antinode_pos(*pair)
            for antinode in antinodes_:
                if (0 <= antinode[0] < WIDTH) and (0 <= antinode[1] < HEIGHT):
                    antinodes.add(antinode)
    return antinodes

antinodes = find_antinodes()
print("Part 1:", len(antinodes))

def print_antinodes(nodes):
    """debug"""
    input_copy = input.copy()
    for antinode in nodes:
        x, y = antinode
        input_copy[y] = input_copy[y][:x] + "#" + input_copy[y][x+1:]
    print("\n".join(input_copy))

def is_in_range(pos: position) -> bool:
    return (0 <= pos[0] < WIDTH) and (0 <= pos[1] < HEIGHT)

def calc_resonant_antinode_pos(pos1: position, pos2: position) -> list[position]:
    result: list[position] = []

    diff: position = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    base: position = pos1
    while(True):
        antinode: position = (base[0] - diff[0], base[1] - diff[1])
        if not is_in_range(antinode):
            break
        base = antinode
        result.append(antinode)

    base = pos2
    while(True):
        antinode: position = (base[0] + diff[0], base[1] + diff[1])
        if not is_in_range(antinode):
            break
        base = antinode
        result.append(antinode)

    result.append(pos1)
    result.append(pos2)

    return result

def find_resonant_antinodes() -> set[position]:
    antinodes: set[position] = set()
    for antenna_type, positions in antennas.items():
        pairs = itertools.combinations(positions, 2)
        for pair in pairs:
            antinodes_= calc_resonant_antinode_pos(*pair)
            antinodes.update(antinodes_)
    return antinodes

resonant_antinodes = find_resonant_antinodes()
print("Part 2:", len(resonant_antinodes))
# print(resonant_antinodes)

# print_antinodes(resonant_antinodes)
