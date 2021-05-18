def parse_values(cell, d_values):
    lines = cell.split("\n")
    for line in lines:
        if "=" in line:
            val = line.split("=")
            if len(val) == 2:
                val[0] = val[0].strip()
                val[1] = val[1].strip()
                d_values[val[0]] = val[1]


TEXT = "# Exclude\n" \
       "x = 0\n" \
       "y1 = 2\n" \
       "z3 = 1.1e-3   \n"


def main():
    d_values = {}
    parse_values(TEXT, d_values)
    print(d_values)


if __name__ == "__main__":
    main()
