from sympy import *
from variable_recognition import Variable
from parse_pack import Pack

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_derivatives(var, pack):
    der = []
    ns = {}
    var.equation = format_equation(var.equation, pack)
    for p in get_input_param(var, []):
        ns[p.symbol] = Symbol(p.symbol)
    eq_str = parse_eq_rec(var, pack)
    try:
        eq = sympify(eq_str, locals=ns)
        for key in ns:
            derv = str(diff(eq, ns[key]))
            der.append(format_derivative(derv))
    except SympifyError:
        for key in ns:
            der.append("# sympy could not parse the equation")
    return der


def parse_eq_rec(var, pack):
    eq_str = format_equation(var.equation, pack)
    for p in var.param:
        if p.output:
            eq_str = eq_str.replace(p.symbol, '(' + parse_eq_rec(p, pack) + ')')
    return eq_str


def get_input_param(var, param):
    param_ = param
    for p in var.param:
        if p not in param_:
            if not p.output:
                param_.append(p)
            else:
                param_ = get_input_param(p, param_)
    return param_


def format_equation(eq_str, pack):
    for p in pack:
        if p.short:
            pre = p.nick + "."
        else:
            pre = p.name + "."
        eq_str = eq_str.replace(pre, "")
    return eq_str


def format_derivative(der):
    f = {}
    for i in range(len(der)):
        if der[i] == "(":
            func = ""
            j = 1
            while j <= i and der[i-j] in LETTERS:
                func = der[i-j] + func
                j += 1
            if func != "":
                if func not in f:
                    f[func] = 1
                else:
                    f[func] += 1
    for func in f:
        der = der.replace(func, "np." + func, f[func])
    return der


DER = "1/(x+sin(y)"

p1 = Pack(name="numpy", short=True, nick="np")
p2 = Pack(name="mat", short=False, nick="")
packs = [p1, p2]

expr = "np.log(y) + mat.exp(z**2) + np.sin(u)"
expr2 = "y**2 + np.cos(z)"

var1 = Variable("x", output=True)
var2 = Variable("y")
var3 = Variable("z")
var4 = Variable("u", output=True)

var1.add_param(var2)
var1.add_param(var3)
var1.add_param(var4)
var4.add_param(var2)
var4.add_param(var3)

var1.equation = expr
var4.equation = expr2


def main():
    print(get_derivatives(var1, packs))
    print(format_derivative(DER))


if __name__ == "__main__":
    main()
