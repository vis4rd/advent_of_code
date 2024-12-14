import re
from dataclasses import dataclass
from math import floor

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for second, line in enumerate(input):
        input[second] = line.replace("\n", "")


@dataclass
class vec2:
    x: int
    y: int


@dataclass
class Button:
    shift: vec2
    cost: int


@dataclass
class Machine:
    a_button: Button
    b_button: Button
    prize: vec2


def parse_input(input: list[str]) -> list[Machine]:
    result = []

    for i in range(0, len(input), 4):
        line_1 = input[i]
        line_2 = input[i + 1]
        line_3 = input[i + 2]

        l1_matches = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line_1)
        l2_matches = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line_2)
        l3_matches = re.match(r"Prize: X=(\d+), Y=(\d+)", line_3)

        if l1_matches and l2_matches and l3_matches:
            a_button = Button(
                vec2(int(l1_matches.group(1)), int(l1_matches.group(2))), 3
            )
            b_button = Button(
                vec2(int(l2_matches.group(1)), int(l2_matches.group(2))), 1
            )
            prize = vec2(int(l3_matches.group(1)), int(l3_matches.group(2)))

            machine: Machine = Machine(a_button, b_button, prize)
            result.append(machine)

    return result


machines: list[Machine] = parse_input(input)


def solve_machine(machine: Machine) -> tuple[int, int] | None:
    ax_in_prize: int = machine.prize.x // machine.a_button.shift.x
    ay_in_prize: int = machine.prize.y // machine.a_button.shift.y
    max_a_button_presses: int = min(ax_in_prize, ay_in_prize, 100)

    for a_button_presses in range(max_a_button_presses, -1, -1):
        a_button_prize_filled: vec2 = vec2(
            a_button_presses * machine.a_button.shift.x,
            a_button_presses * machine.a_button.shift.y,
        )
        bx_in_remainder_cnt: int = (
            machine.prize.x - a_button_prize_filled.x
        ) // machine.b_button.shift.x
        by_in_remainder_cnt: int = (
            machine.prize.y - a_button_prize_filled.y
        ) // machine.b_button.shift.y

        if bx_in_remainder_cnt < 1 or by_in_remainder_cnt < 1:
            continue

        if bx_in_remainder_cnt != by_in_remainder_cnt:
            continue

        if (
            (bx_in_remainder_cnt * machine.b_button.shift.x)
            == (machine.prize.x - a_button_prize_filled.x)
        ) and (
            (by_in_remainder_cnt * machine.b_button.shift.y)
            == (machine.prize.y - a_button_prize_filled.y)
        ):
            return (a_button_presses, bx_in_remainder_cnt)

    return None


def calculate_token_cost(machine: Machine) -> int:
    solution = solve_machine(machine)
    if solution:
        return machine.a_button.cost * solution[0] + machine.b_button.cost * solution[1]
    else:
        return 0


def all_machine_costs(machines: list[Machine]) -> int:
    return sum(calculate_token_cost(machine) for machine in machines)


print("Part 1:", all_machine_costs(machines))

# part 2
machines_2: list[Machine] = machines.copy()
for machine in machines_2:
    machine.prize.x += 10000000000000
    machine.prize.y += 10000000000000


def solve_machine_2(machine: Machine) -> tuple[int, int] | None:
    b_amount = (
        machine.prize.y * machine.a_button.shift.x
        - machine.prize.x * machine.a_button.shift.y
    ) / (
        machine.b_button.shift.y * machine.a_button.shift.x
        - machine.b_button.shift.x * machine.a_button.shift.y
    )
    a_amount = (
        machine.prize.x - b_amount * machine.b_button.shift.x
    ) / machine.a_button.shift.x

    if floor(a_amount) == a_amount and floor(b_amount) == b_amount:
        return (int(a_amount), int(b_amount))

    return None


def calculate_token_cost_2(machine: Machine) -> int:
    solution = solve_machine_2(machine)
    if solution:
        return machine.a_button.cost * solution[0] + machine.b_button.cost * solution[1]
    else:
        return 0


def all_machine_costs_2(machines: list[Machine]) -> int:
    return sum(calculate_token_cost_2(machine) for machine in machines)


print("Part 2:", all_machine_costs_2(machines_2))
