from copy import copy

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

space_map: str = "".join(input)

def construct_memory_layout() -> list[int | str]:
    blocks: list[int | str] = []
    id = 0
    for i, c in enumerate(space_map):
        if i % 2 == 0:
            [blocks.append(int(id)) for _ in range(int(c))]
            id += 1
        else:
            [blocks.append('.') for _ in range(int(c))]
    return blocks

layout = construct_memory_layout()

def calculate_tight_layout_length(layout: list[int | str]) -> int:
    sum_: int = 0
    for i, c in enumerate(space_map):
        if i % 2 == 0:
            sum_ += int(c)
    return sum_

def is_layout_tight(layout: list[int | str]) -> bool:
    for i in range(len(layout) - 1):
        if layout[i] == '.' and layout[i + 1] != '.':
            return False
    return True

def tighten_layout(layout: list[int | str]) -> list[int | str]:
    new_layout: list[int | str] = []
    target_length: int = calculate_tight_layout_length(layout)
    rev_i: int = 1

    def find_next_id_from_back(layout: list[int | str], rev_i: int) -> tuple[int, int]:
        for i in range(rev_i, len(layout)):
            if layout[-i] != '.':
                return layout[-i], rev_i
            else:
                rev_i += 1
        return '.', rev_i

    for i in range(len(layout)):
        if layout[i] != '.':
            new_layout.append(layout[i])
        else:
            id_from_back, rev_i = find_next_id_from_back(layout, rev_i)
            new_layout.append(id_from_back)
            rev_i += 1

        if len(new_layout) == target_length:
            break
    return new_layout

tight_layout = tighten_layout(layout)

def calculate_layout_checksum(layout: list[int | str]) -> int:
    sum_: int = 0
    for i in range(len(layout)):
        if layout[i] == '.':
            continue
        sum_ += i*layout[i]
    return sum_

print("Part 1:", calculate_layout_checksum(tight_layout))

# part 2

def print_layout(layout: list[int | str]) -> None:
    """debug"""
    print("".join([str(c) for c in layout]))


class MemoryBlock:
    def __init__(self, id: int | str, size: int) -> None:
        self.id: int | str = id
        self.size: int = size
    def __str__(self) -> str:
        return f"({self.id}, {self.size})"
    def __repr__(self) -> str:
        return self.__str__()

def construct_memory_blocks() -> list[MemoryBlock]:
    blocks: list[MemoryBlock] = []
    i = 0
    while i < len(space_map):
        blocks.append(MemoryBlock(i // 2, int(space_map[i])))
        if (i + 1) < len(space_map):
            blocks.append(MemoryBlock('.', int(space_map[i + 1])))
        i += 2
    return blocks

def tighten_blocks(blocks: list[MemoryBlock]) -> list[MemoryBlock]:
    for rev_i in range(blocks[-1].id, -1, -1):
        file_idx: int = next(idx for idx, el in enumerate(blocks) if el.id == rev_i)
        for fit_space_idx in range(file_idx):
            if (blocks[fit_space_idx].id == '.') and (blocks[fit_space_idx].size >= blocks[file_idx].size):
                blocks[fit_space_idx].size -= blocks[file_idx].size
                blocks.insert(fit_space_idx, copy(blocks[file_idx]))
                blocks[file_idx + 1].id = '.'
                break
    return blocks

def convert_blocks_to_layout(blocks: list[MemoryBlock]) -> list[int | str]:
    layout: list[int | str] = []
    for block in blocks:
        [layout.append(block.id) for _ in range(block.size)]
    return layout

blocks = construct_memory_blocks()
tight_blocks = tighten_blocks(blocks)
tight_blocks_layout = convert_blocks_to_layout(tight_blocks)
print("Part 2:", calculate_layout_checksum(tight_blocks_layout))
