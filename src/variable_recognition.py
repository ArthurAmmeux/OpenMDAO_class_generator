import re

RE_SYMBOLS = r"[-=+*/%><)\s\t]+"
KEYWORDS = [":", "if", "else", "elif", "True", "False"]
PARENTHESES = ["("]
DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
LETTERS = "abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMONPQRSTUVWXYZ"


def string_to_list(str):
    lis = []
    for c in str:
        lis.append(c)
    return lis


def contains(e, sym):
    for s in sym:
        if s in e:
            return True
    return False


def does_not_contain(e, sym):
    for s in sym:
        if s in e:
            return False
    return True


def is_not_in(e, lis):
    for x in lis:
        if e == x:
            return False
    return True


def handle_function(x, var_in, var_out):
    if does_not_contain(x, PARENTHESES):
        letters = string_to_list(LETTERS)
        p = re.split(RE_SYMBOLS, x)
        for y in p:
            if is_not_in(y, KEYWORDS) and is_not_in(y, var_in) and is_not_in(y, var_out):
                if contains(y, letters):
                        var_in.append(x)
    else:
        f = re.split(r'[(]', x, 1)
        if contains('', f):
            f.remove('')
        if len(f) == 2:
            handle_function(f[1], var_in, var_out)


def get_variables(equation):
    letters = string_to_list(LETTERS)
    var_in = []
    var_out = []
    lines = equation.splitlines()
    groups = []
    for line in lines:
        groups.append(re.split(RE_SYMBOLS, line))
    for line_ in groups:

        if contains('', line_):
            line_.remove('')

        first = True
        if not is_not_in(line_[0], KEYWORDS):
            first = False

        for x in line_:
            if is_not_in(x, KEYWORDS) and is_not_in(x, var_in) and is_not_in(x, var_out):
                if does_not_contain(x, PARENTHESES):
                    if contains(x, letters):
                        if first:
                            var_out.append(x)
                            first = False
                        else:
                            var_in.append(x)
                else:
                    if contains(x, letters):
                        handle_function(x, var_in, var_out)
                        first = False
    return var_in, var_out


def edit_function(inputs, outputs, function):
    prefix = ""
    suffix = "\n"

    for i in range(len(inputs)):
        prefix += "{} = inputs['{}']\n".format(inputs[i][0], inputs[i][1])
    prefix += "\n"

    for i in range(len(outputs)):
        suffix += "outputs['{}'] = {}\n".format(outputs[i][1], outputs[i][0])

    return prefix + function + suffix

