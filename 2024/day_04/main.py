with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

    def xmas_in_one_line(line: str) -> int:
        return line.count("XMAS") + line[::-1].count("XMAS")

    def xmas_in_lines(input: list[str]) -> int:
        sum_: int = 0
        for line in input:
            sum_ += xmas_in_one_line(line)
        return sum_

    # horizontal search
    sum_h: int = xmas_in_lines(input)

    # vertical search
    input_transposed: list[str] = [
        "".join([line[i] for line in input]) for i in range(len(input[0]))
    ]
    sum_v: int = xmas_in_lines(input_transposed)

    # diagonal search
    def get_diagonals(input: list[str]) -> list[str]:
        diagonals = []
        rows, cols = len(input), len(input[0])

        for d in range(rows + cols - 1):
            diagonal_nw_se = []  # top-left to bottom-right
            diagonal_ne_sw = []  # top-right to bottom-left
            for row in range(max(0, d - cols + 1), min(rows, d + 1)):
                col_e = d - row
                col_w = cols - 1 - (d - row)
                diagonal_nw_se.append(input[row][col_e])
                diagonal_ne_sw.append(input[row][col_w])
            diagonals.append("".join(diagonal_nw_se))
            diagonals.append("".join(diagonal_ne_sw))

        return diagonals

    input_diagonals = get_diagonals(input)
    sum_d = xmas_in_lines(input_diagonals)

    # part 1
    xmas_sum = sum_h + sum_v + sum_d
    print(f"part 1: {xmas_sum}")

    # part 2
    mas_sum: int = 0
    for i in range(1, len(input)-1):
        for j in range(1, len(input[0])-1):
                center = input[i][j]
                top_left = input[i - 1][j - 1]
                top_right = input[i - 1][j + 1]
                bottom_left = input[i + 1][j - 1]
                bottom_right = input[i + 1][j + 1]

                tl_br: str = top_left + center + bottom_right
                tr_bl: str = top_right + center + bottom_left

                if (tl_br in ["MAS", "SAM"]) and (tr_bl in ["MAS", "SAM"]):
                    mas_sum += 1
    print(f"part 2: {mas_sum}")
