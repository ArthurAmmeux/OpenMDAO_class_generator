import re

RE_SYMBOLS = r"[-=+*/%><)\s\t]+"
KEYWORDS = [":", "if", "else", "elif", "True", "False", "np.pi"]
PARENTHESES = ["("]
DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
LETTERS = "abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMONPQRSTUVWXYZ"
PACKAGES = ["numpy.", "np.", "mat.", "math."]


def string_to_list(str):
    """
    :param str: input string
    :return: a list of the characters in the input string
    """
    lis = []
    for c in str:
        lis.append(c)
    return lis


def contains(e, sym):
    """
    :param e: string to be tested
    :param sym: string that could be in e
    :return: True if any of the chars in sym is in e
    """
    for s in sym:
        if s in e:
            return True
    return False


def does_not_contain(e, sym):
    """
    :param e: string to be tested
    :param sym: string that could be in e
    :return: False if any of the chars in sym is in e
    """
    for s in sym:
        if s in e:
            return False
    return True


def is_not_in(e, lis):
    """
    :param e: potential element of lis
    :param lis: list to be tested
    :return: True if e is not in lis
    """
    for x in lis:
        if e == x:
            return False
    return True


def check_pack(x):
    """
    :param x: potential variable to be tested
    :return: checks if the variable is not a constant from a package
    """
    for pack in PACKAGES:
        l = len(pack)
        if len(x) >= l:
            if x[0:l] == pack:
                return False
    return True


def add_var_in(x, var_in, var_out):
    """
    :param x: potential variable to add
    :param var_in: list of input variables already added
    :param var_out: list of output variables already added
    :return: adds the variable to var_in if the conditions are verified and returns True if the variable has been added
    """
    if is_not_in(x, KEYWORDS) and is_not_in(x, var_in) and is_not_in(x, var_out) and check_pack(x):
        var_in.append(x)
        return True
    return False


def add_var_out(x, var_in, var_out):
    """
    :param x: potential variable to add
    :param var_in: list of input variables already added
    :param var_out: list of output variables already added
    :return: adds the variable to var_out if the conditions are verified and returns True if the variable has been added
    """
    if is_not_in(x, KEYWORDS) and is_not_in(x, var_in) and is_not_in(x, var_out) and check_pack(x):
        var_out.append(x)
        return True
    return False


def handle_function(x, var_in, var_out):
    """
    :param x: string with functions in which to find variables
    :param var_in: input variables already found
    :param var_out: output variables already found
    :return: adds the newly found variables to var_in
    """
    if x[0] == '(':
        x = x[1:]
        if len(x) > 1 and x[-1] == 'e':
            handle_exponent(x, var_in, var_out)
        add_var_in(x, var_in, var_out)

    if does_not_contain(x, PARENTHESES):
        letters = string_to_list(LETTERS)
        p = re.split(RE_SYMBOLS, x)
        for y in p:
            if contains(y, letters):
                if len(x) > 1 and x[-1] == 'e':
                    handle_exponent(x, var_in, var_out)
                elif is_not_in(x, var_in) and is_not_in(x, var_out):
                    add_var_in(x, var_in, var_out)
    else:
        f = re.split(r'[(]', x, 1)
        if contains('', f):
            f.remove('')
        if len(f) == 2:
            handle_function(f[1], var_in, var_out)


def handle_exponent(x, var_in, var_out):
    """
    :param x: string with potential exponent
    :param var_in: input variables already found
    :param var_out: output variables already found
    :return: adds the newly found variables to var_in
    """
    y = x[:-1]
    if contains(y, LETTERS) or does_not_contain(y, DIGITS):
        add_var_in(x, var_in, var_out)


def get_variables(equation):
    """
    :param equation: string of equations written in python syntax potentially with functions
    :return: input and output variables found in equation + default names which are the same as the original
    """
    letters = string_to_list(LETTERS)
    var_in = []
    var_out = []
    units_out = []
    units_o = []
    lines = equation.splitlines()
    groups = []
    for i in range(len(lines)):
        spt = re.split(r'[#[]', lines[i])
        if len(spt) >= 2:
            unit = spt[-1]
            if len(unit) > 1:
                units_out.append([i, unit[:-1]])
            else:
                units_out.append([i, ''])
            lines[i] = spt[0]
    for i in range(len(lines)):

        first = True
        if '=' not in lines[i]:
            first = False
        groups = (re.split(RE_SYMBOLS, lines[i]))
        if '' in groups:
            groups.remove('')
        if not is_not_in(groups[0], KEYWORDS):
            first = False

        for x in groups:
            if does_not_contain(x, PARENTHESES):
                if contains(x, letters):
                    if first:
                        added = add_var_out(x, var_in, var_out)
                        if added:
                            u_out = 'None'
                            for u in units_out:
                                if u[0] == i:
                                    u_out = u[1]
                            units_o.append(u_out)
                    else:
                        if len(x) > 1 and x[-1] == 'e':
                            handle_exponent(x, var_in, var_out)
                        else:
                            add_var_in(x, var_in, var_out)
            else:
                if contains(x, letters):
                    handle_function(x, var_in, var_out)
            first = False

    var_in_ = [[x, x + "_name"] for x in var_in]
    var_out_ = [[x, x + "_name"] for x in var_out]
    return var_in_, var_out_, units_o


def format_line(line):
    """
    :param line: line to be modified
    :return: removes spaces before and after the name
    """
    while len(line) > 1 and line[0] == ' ':
        line = line[1:]
    while len(line) > 1 and line[-1] == ' ':
        line = line[:-1]
    return line


def edit_function(inputs, outputs, function):
    """
    :param inputs: list of input variables with their new name
    :param outputs: list of output variables with their new name
    :param function: original equations
    :return: a function compatible with the compute function of om.Component
    """
    prefix = ""
    suffix = "\n"

    lines = function.splitlines()
    for i in range(len(lines)):
        lines[i] = format_line(lines[i])
    function_ = ""
    for line in lines:
        function_ += line + "\n"

    for i in range(len(inputs)):
        prefix += "{} = inputs['{}']\n".format(inputs[i][0], inputs[i][1])
    prefix += "\n"

    for i in range(len(outputs)):
        suffix += "outputs['{}'] = {}\n".format(outputs[i][1], outputs[i][0])

    return prefix + function_ + suffix

