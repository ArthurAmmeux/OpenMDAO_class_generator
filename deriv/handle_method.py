import variable_recognition as vr
import re


class Method:
    """
    A class to store data about methods
    """
    def __init__(self, name, arg_names=None, equation="", rtn=""):
        self.name = name
        self.arg_names = arg_names
        self.equation = equation
        self.rtn = rtn


class MethodCall:
    """
    A class to store data about method calls
    """
    def __init__(self, method, args=None, call=""):
        self.method = method
        self.args = args
        self.call = call


def handle_method(method_calls, equations, str, pack):
    """
    :param method_calls: list of calls of a method
    :param equations: the equations of the compute function
    :param str: the string in which to find methods
    :param pack: list of packs used
    :return:
    """
    methods = []
    calls = []
    for method_call in method_calls:
        name, args = parse_call(method_call)
        method = Method(name)
        add = True
        for m in methods:
            if m.name == method.name:
                add = False
        if add:
            methods.append(method)
        calls.append(MethodCall(method, args=args, call=method_call))

    for method in methods:
        equation, args = find_method(method.name, str)
        method.equation = equation
        method.arg_names = args
        method.rtn = parse_method(equation, pack)

    new_equations = equations

    for call in calls:
        rtn = call.method.rtn
        arg_names = call.method.arg_names
        args = call.args
        new_rtn = "(" + use_args(args, arg_names, rtn) + ")"
        new_equations = equations.replace(call.call, new_rtn)

    return new_equations


def find_method(name, str):
    """
    :param name: method name
    :param str: the string in which to find the method
    :return: a list of the arguments and the code of the method
    """
    match = re.search("def " + name + r"\([\w, ]*\):", str)
    args = re.split(r',\s*', match[0].split("(", 1)[1][:-2])
    args = [arg.strip() for arg in args]
    if "self" in args:
        args.remove("self")
    met = str[match.end():]
    match2 = re.search(r'"""[^"]*"""', met)
    if match2:
        met = met[match2.end():]
    match3 = re.search(r'return [^\n]+', met)
    if match3:
        met = met[:match3.end()]
    return met, args


def parse_call(method_call):
    """
    :param method_call: string containing a method call
    :return: the name of the method and a list of the arguments
    """
    spt = method_call.split("(", 1)
    method = spt[0][5:]
    args = re.split(r",\s*", spt[1][:-1])
    args = [arg.strip() for arg in args]
    return method, args


def parse_method(met, pack):
    """
    :param met: the method code
    :param pack: packs used
    :return: a single line encompassing the entire method with only arguments as variables
    """
    lines = met.splitlines()
    rtn = ""
    for line in lines:
        if '#' in line:
            line = line.split('#')[0].strip()
        if "return " in line:
            rtn = line.split("return")[1]
    if len(lines) > 1:
        eq = ""
        for i in range(len(lines)-1):
            eq += lines[i] + "\n"
        var_in, var_out, const = vr.get_variables(eq, pack)
        expr = []
        for v_out in var_out:
            expr.append([v_out.symbol, parse_eq_rec(v_out)])
        for i in range(len(expr)):
            rtn = replace_symbol(expr[i][0], expr[i][1], rtn)
    return rtn.strip()


def use_args(args, arg_names, rtn):
    """
    :param args: arguments from call
    :param arg_names: name of the arguments in the  function definition
    :param rtn: the parsed method as a single line expression
    :return: an expression of the parsed method with the arguments from the call
    """
    func = rtn
    if len(args) == len(arg_names):
        for i in range(len(args)):
            func = replace_symbol(arg_names[i], args[i], func)
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
    """
    :param sym: symbol to be replaced
    :param rep: replacement
    :param exp: expression
    :return: replaces sym with (rep) as long as sym is a word
    """
    return re.sub(r'(?<=\b)' + sym + r'(?=\b)', '(' + rep + ')', exp)


MET = "y = x + 1\n" \
      "z =y**2 + 2*y\n" \
      "return z + y - 1"

equations = """
a = (self.plus((x ** 2), (u)))
y = np.pi * a
z = np.sin(a)
"""


def main():
    # print(parse_method(MET, []))
    # print(parse_call("self.cosinus(  var1, var2,var3,   var4  )"))
    f = open("testMethod.py")
    test_str = f.read()
    # tup = find_method("_get_thickness", test_str)
    # print(tup[0])
    # print(tup[1])
    method_calls_iter = re.finditer(r'self.\w+\([\w, (*/+-]*\)', equations)
    method_calls = []
    for match in method_calls_iter:
        print(match)
        op = match[0].count("(")
        cl = match[0].count(")")
        index = match.end()
        method_call = match[0]
        while op != cl:
            method_call += equations[index]
            op = method_call.count("(")
            cl = method_call.count(")")
            index += 1
        method_calls.append(method_call)
    print(method_calls)
    print(handle_method(method_calls, equations, test_str, []))


if __name__ == '__main__':
    main()
