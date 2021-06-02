from sympy import *
from variable_recognition import Variable
from parse_pack import Pack


def get_derivatives(var, pack):
    der = []
    ns = {}
    for p in var.param:
        ns[p.symbol] = Symbol(p.symbol)
    eq_str = var.equation
    for p in pack:
        if p.short:
            pre = p.nick + "."
        else:
            pre = p.name + "."
        eq_str = eq_str.replace(pre, "")
    try:
        eq = sympify(eq_str, locals=ns)
        for key in ns:
            der.append(str(diff(eq, ns[key])))
    except SympifyError:
        for key in ns:
            der.append("# sympy could not parse the equation")
    return der


p1 = Pack(name="numpy", short=True, nick="np")
p2 = Pack(name="mat", short=False, nick="")
pack = [p1, p2]

expr = "np.log(y) + mat.exp(z**2) + 1"

var1 = Variable("x")
var2 = Variable("y")
var3 = Variable("z")
var1.add_param(var2)
var1.add_param(var3)
var1.equation = expr


def main():
    print(get_derivatives(var1, pack))


if __name__ == "__main__":
    main()
