import re

RE_SYMBOLS = r"[-=+*/%><):\s\t]+"
KEYWORDS = [":", "if", "else", "elif", "if:", "else:", "elif:", "True", "False", "True:", "False:"]
PARENTHESES = ["("]
DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMONPQRSTUVWXYZ"
PACKAGES = ["numpy.", "np.", "mat.", "math."]


class Variable:
    def __init__(self, symbol='Default', name='Default_name', unit='None', val='np.nan', output=False):
        self.symbol = symbol
        self.name = name
        if symbol != 'Default' and name == 'Default_name':
            self.name = symbol + '_name'
        self.unit = unit
        self.val = val
        self.param = []
        self.equation = ""
        self.output = output
        self.deleted = False

    def __str__(self):
        param = "\n"
        for p in self.param:
            param += str(p) + "\n"
        return "symbol: " + self.symbol + " name: " + self.name + " param:( " + param + ")\nequation: " + self.equation

    def add_param(self, param):
        self.param.append(param)

    def delete(self):
        self.deleted = True


class Constant:
    def __init__(self, symbol):
        self.full = symbol
        rev = symbol[::-1]
        split_rev = rev.split(".", maxsplit=1)
        self.short = split_rev[0][::-1]
        self.pack = split_rev[1][::-1]


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


def not_var(x, var_list):
    """
    :param x: string to test
    :param var_list: list of variables
    :return: returns True if x is not a symbol of one of the variables in var_list
    """
    for var in var_list:
        if x == var.symbol:
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


def check_pack(x, pack):
    """
    :param pack: list of packages that the user wants to import (instances of Pack class)
    :param x: potential variable to be tested
    :return: checks if the variable is not a constant from a package
    """
    packages = []
    if len(pack) > 0:
        for p in pack:
            if p.short:
                packages.append(p.nick + ".")
            else:
                packages.append(p.name + ".")

        for p in packages:
            l = len(p)
            if len(x) >= l:
                if x[0:l] == p:
                    return False
    return True


def format_const(const):
    """
    :param const: list of constants with multiple occurrences of the same element
    :return: a reformatted list without multiple occurrences of the same element
    """
    const_ = []
    for c in const:
        dif = True
        for d in const_:
            if c == d:
                dif = False
        if dif:
            const_.append(c)
    return const_


def add_var_in(x, var_in, var_out, const, pack, add_p=False):
    """
    :param add_p: boolean to know if the variable should be added as a parameter
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param x: potential variable to add
    :param var_in: list of input variables already added
    :param var_out: list of output variables already added
    :param const: constants already found
    :return: adds the variable to var_in if the conditions are verified and returns True if the variable has been added
    also returns the variable added if a variable was added
    """
    out_added = len(var_out) > 0
    if is_not_in(x, KEYWORDS):
        if check_pack(x, pack):
            if not_var(x, var_in) and not_var(x, var_out):
                var = Variable(symbol=x, output=False)
                if add_p and out_added:
                    var_out[-1].add_param(var)
                var_in.append(var)
                return [True, var]
            elif out_added:
                last_out = var_out[-1]
                for v_in in var_in:
                    if x == v_in.symbol:
                        for param in last_out.param:
                            if x == param.symbol:
                                return [False, None]
                        var_out[-1].add_param(v_in)
                        return [False, v_in]
                for v_out in var_out:
                    if x == v_out.symbol:
                        for param in last_out.param:
                            if x == param.symbol:
                                return [False, None]
                        if x != var_out[-1].symbol:
                            var_out[-1].add_param(v_out)
                            return [False, v_out]
                        return [False, None]
        else:
            const.append(Constant(x))
    return [False, None]


def add_var_out(x, var_in, var_out, pack):
    """
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param x: potential variable to add
    :param var_in: list of input variables already added
    :param var_out: list of output variables already added
    :return: adds the variable to var_out if the conditions are verified and returns True if the variable has been added
    also returns the variable added if a variable was added
    """
    if is_not_in(x, KEYWORDS) and not_var(x, var_in) and not_var(x, var_out) and check_pack(x, pack):
        var = Variable(symbol=x, val='', output=True)
        var_out.append(var)
        return [True, var]
    return [False, 'None']


def handle_function(x, var_in, var_out, const, pack):
    """
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param x: string with functions in which to find variables
    :param var_in: input variables already found
    :param var_out: output variables already found
    :param const: constants already found
    :return: adds the newly found variables to var_in
    """
    if x[0] == '(' and len(x) > 1:
        handle_function(x[1:], var_in, var_out, const, pack)

    elif does_not_contain(x, PARENTHESES):
        letters = string_to_list(LETTERS)
        p = re.split(RE_SYMBOLS, x)
        for y in p:
            if contains(y, letters):
                if len(x) > 1 and x[-1] == 'e':
                    handle_exponent(x, var_in, var_out, const, pack)
                else:
                    add_var_in(x, var_in, var_out, const, pack, True)
    else:
        f = re.split(r'[(]', x, 1)
        if contains('', f):
            f.remove('')
        if len(f) == 2:
            handle_function(f[1], var_in, var_out, const, pack)


def handle_exponent(x, var_in, var_out, const, pack):
    """
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param x: string with potential exponent
    :param var_in: input variables already found
    :param var_out: output variables already found
    :param const: constants already found
    :return: adds the newly found variables to var_in
    """
    y = x[:-1]
    if contains(y, LETTERS) or does_not_contain(y, DIGITS):
        add_var_in(x, var_in, var_out, const, pack, True)


def get_variables(equation, pack):
    """
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param equation: string of equations written in python syntax potentially with functions
    :return: input and output variables found in equation + default names which are the same as the original as well
    as the constants found
    """
    letters = string_to_list(LETTERS)
    var_in = []
    var_out = []
    const = []
    units_out = []
    lines = equation.splitlines()
    for i in range(len(lines)):
        spt = lines[i].split('# [')
        if len(spt) >= 2:
            unit = spt[-1]
            if len(unit) > 1:
                f_unit = unit.split("]")[0]
                units_out.append([i, f_unit])
            else:
                units_out.append([i, ''])
            lines[i] = spt[0]
    for i in range(len(lines)):
        spt = lines[i].split('#[')
        if len(spt) >= 2:
            unit = spt[-1]
            if len(unit) > 1:
                f_unit = unit.split("]")[0]
                units_out.append([i, f_unit])
            else:
                units_out.append([i, 'None'])
            lines[i] = spt[0]
    added = False
    for i in range(len(lines)):
        first = True
        if '=' not in lines[i]:
            first = False
        else:
            added = False
        if '#' in lines[i]:
            lines[i] = lines[i].split('#', 1)[0]
        if '"""' in lines[i]:
            lines[i] = lines[i].split('"""', 1)[0]
        if "'''" in lines[i]:
            lines[i] = lines[i].split("'''", 1)[0]
        groups = re.split(RE_SYMBOLS, lines[i])
        if '' in groups:
            groups.remove('')
        if len(groups) > 0 and not is_not_in(groups[0], KEYWORDS):
            first = False
            added = False
        if added:
            var_out[-1].equation += lines[i]

        for x in groups:
            if does_not_contain(x, PARENTHESES):
                if contains(x, letters):
                    if first:
                        [added, var] = add_var_out(x, var_in, var_out, pack)
                        if added:
                            u_out = 'None'
                            for u in units_out:
                                if u[0] == i:
                                    u_out = u[1]
                            var.unit = u_out
                            var.equation = lines[i].split("=")[1]
                    else:
                        if len(x) > 1 and x[-1] == 'e':
                            handle_exponent(x, var_in, var_out, const, pack)
                        else:
                            add_var_in(x, var_in, var_out, const, pack, True)
            else:
                if contains(x, letters):
                    handle_function(x, var_in, var_out, const, pack)
            first = False

    const = format_const(const)

    return var_in, var_out, const


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
    function_ = ""
    for line in lines:
        function_ += line + "\n"

    for i in range(len(inputs)):
        prefix += "{} = inputs['{}']\n".format(inputs[i].symbol, inputs[i].name)
    prefix += "\n"

    for i in range(len(outputs)):
        suffix += "outputs['{}'] = {}\n".format(outputs[i].name, outputs[i].symbol)

    return prefix + function_ + suffix


TEXT = "y = x + 1 # [kg] Mass\n" \
       "theta = 1 + (tan(sweep_25 / 180.0 * pi)) ** 2\n" \
       "if y == 0:\n" \
       "    y = 1\n" \
       "z = 1 + (sin(tan(y**2) - cos(ch(x))))**2\n" \
       "# Comment here\n"


def main():
    var_in, var_out, const = get_variables(TEXT, [])
    l_in = [v.symbol for v in var_in]
    l_out = [v.symbol for v in var_out]
    print(l_in)
    print(l_out)


if __name__ == '__main__':
    main()