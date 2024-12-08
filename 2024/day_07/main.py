from itertools import product
from typing import Callable

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

test_values: list[int] = [int(line.split(":")[0]) for line in input]

equations: list[list[int]] = [
    [int(num) for num in line.split(":")[1].split(" ") if num != ""] for line in input
]

OPS_MAPPER: dict[str, Callable] = {
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
    "|": lambda x, y: int(f"{x}{y}"), # comment this line for part 1
}


def test_equation(equation: list[int], test_value: int, ops: str) -> bool:
    result: int = equation[0]
    for i in range(1, len(equation)):
        result = OPS_MAPPER[ops[i - 1]](result, equation[i])
    return result == test_value


ok_equations_count: int = 0
sum_: int = 0
for test_value, equation in zip(test_values, equations):
    ops_permutations: list[str] = [
        "".join(p)
        for p in product("".join(list(OPS_MAPPER.keys())), repeat=len(equation) - 1)
    ]
    for ops in ops_permutations:
        if test_equation(equation, test_value, ops):
            ok_equations_count += 1
            sum_ += test_value
            break

print(ok_equations_count, sum_)
