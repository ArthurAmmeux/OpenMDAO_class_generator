import derivative as d
import subprocess
from textwrap import indent


def derivative_str(inputs, outputs, const, pack):
    """
    :param inputs: list of input variables "renamed"
    :param outputs: list of output variables "renamed"
    :param const: list of constants present in the component
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :return: a string containing the code of an om.Component
    """
    ls = []
    s = "setup_partials(self):\n"
    for var_out in outputs:
        for p in var_out.param:
            if p.deleted and not p.output:
                var_out.param.remove(p)
        input_param = d.get_input_param(var_out, [])
        if len(input_param) > 0:
            if len(input_param) == 1:
                param_name = "'{}'".format(var_out.param[0].name)
            else:
                param_name = "["
                for p in input_param:
                    param_name += "'{}', ".format(p.name)
                param_name = param_name[:-2]
                param_name += "]"
            s += "        self.declare_partials('{}', {})\n".format(var_out.name, param_name)
    ls.append(s)

    c = ""
    c += '    def compute_partials(self, inputs, J, **kwargs):\n'
    for i in range(len(inputs)):
        c += "        {} = inputs['{}']\n".format(inputs[i].symbol, inputs[i].name)
    c += "\n"
    for out in outputs:
        input_param = d.get_input_param(out, [])
        der = d.get_derivatives(out, pack, const)
        for j in range(len(input_param)):
            c += "        J['{}', '{}'] = ".format(out.name, input_param[j].name) + der[j] + "\n"
        c += "\n\n"
    try:
        byt = subprocess.check_output("black --code " + '"' + c + '"')
        byt = byt.replace(b"\r", b"")
        c = byt.decode("ascii")
        c = indent(c, "    ")
    except subprocess.CalledProcessError:
        pass
    ls.append(c)

    return ls
