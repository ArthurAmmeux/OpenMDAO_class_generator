import re


def is_empty(str):
    for l in str:
        if l != '\s' and l != '\n' and l != '\t':
            return False
    return True


def format_str(str):
    lines = str.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    str_ = ""
    for line in non_empty_lines:
        str_ += line + "\n"
    return str_


def parse_comp(str):
    p_str = re.split(r"[#]\s", str)
    components = []

    for x in p_str:
        if is_empty(x):
            p_str.remove(x)

    for c in p_str:
        comp = c.split('\n', 1)
        comp[1] = format_str(comp[1])
        components.append([comp[0], comp[1]])

    return components


TEXT = "\n" \
       "# Component1\n" \
       "\n" \
       "\n" \
       "x = y*3 +2\n" \
       "z = w**2 +a*4\n" \
       "\n" \
       "# Component2\n" \
       "a = b + c*2\n" \
       "d = e + f\n" \
       "\n"


def main():
    print(parse_comp(TEXT))


if __name__ == '__main__':
    main()
