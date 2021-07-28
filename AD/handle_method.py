import variable_recognition as vr
import re


def parse_method(met, pack):
    lines = met.splitlines()
    rtn = ""
    for line in lines:
        if '#' in line:
            line = line.split('#')[0].strip()
        if "return" in line:
            rtn = line.split("return")[1]
    if len(lines) > 1:
        eq = ""
        for i in range(len(lines)-1):
            eq += lines[i] + "\n"
        var_in, var_out, const = vr.get_variables(eq, pack)
        expr = []
        for v_out in var_out:
            expr.append([v_out.symbol, parse_eq_rec(v_out)])
            print(expr)
        for i in range(len(expr)):
            rtn = replace_symbol(expr[i][0], expr[i][1], rtn)
    return rtn.strip()


def use_args(args, args_name, rtn):
    func = rtn
    if len(args) == len(args_name):
        for i in range(len(args)):
            func = replace_symbol(args_name[i], args[i], rtn)
    return func


def parse_eq_rec(var):
    """
    :param var: output variable to get the derivatives from
    :return: an equation where intermediate variables are recursively replaced by their expression relative to input
    variables
    """
    eq_str = var.equation
    for p in var.param:
        if p.output:
            rep = '(' + parse_eq_rec(p) + ')'
            eq_str = re.sub(r'(?<=\b)' + p.symbol + r'(?=\b)', rep, eq_str)
    return eq_str


def replace_symbol(sym, rep, exp):
    return re.sub(r'(?<=\b)' + sym + r'(?=\b)', '(' + rep + ')', exp)


MET = "y = x + 1\n" \
      "z =y**2 + 2*y\n" \
      "return z + y - 1"


def main():
    print(parse_method(MET, []))


if __name__ == '__main__':
    main()
