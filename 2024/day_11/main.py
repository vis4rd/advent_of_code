with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

stones_str: list[str] = input[0].split(" ")
stones: dict[int, int] = {int(stone): 1 for stone in stones_str}

def safe_incr(d: dict[int, int], k: int, val: int) -> None:
    if k not in d:
        d[k] = val
    else:
        d[k] += val

def blink(stones: dict[int, int]) -> dict[int, int]:
    new_stones: dict[int, int] = {}
    for stone, count in stones.items():
        if stone == 0:
            safe_incr(new_stones, 1, count)
        elif (stone_len := len(stone_str := f"{stone}")) % 2 == 0:
            safe_incr(new_stones, int(stone_str[:stone_len//2]), count)
            safe_incr(new_stones, int(stone_str[stone_len//2:]), count)
        else:
            safe_incr(new_stones, stone * 2024, count)

    return new_stones

def perform_n_blinks(stones: dict[int, int], n: int) -> dict[int, int]:
    stones = stones.copy()
    for i in range(n):
        stones = blink(stones)
    return stones

blinked: dict[int, int] = perform_n_blinks(stones, 25)
print("Part 1:", sum(blinked.values()))

superblinked: dict[int, int] = perform_n_blinks(blinked, 50)
print("Part 2:", sum(superblinked.values()))
