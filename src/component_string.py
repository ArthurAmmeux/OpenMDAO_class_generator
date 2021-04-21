from textwrap import indent


def component_str(c_name, inputs, outputs, units_i, units_o, comp_f):
    """
    :param c_name: component name
    :param inputs: list of input variables "renamed"
    :param outputs: list of output variables "renamed"
    :param comp_f: edited computation function
    :return: a string containing the code of an om.Component
    """
    s = ""
    s += "class " + c_name + " (om.ExplicitComponent):\n\n"
    s += "\tdef setup(self):\n"
    for i in range(0, len(inputs)):
        if units_i[i][0] == 'None':
            s += "\t\tself.add_input('{}', val={})\n".format(inputs[i][1], units_i[i][1])
        else:
            s += "\t\tself.add_input('{}', val={}, units='{}')\n".format(inputs[i][1], units_i[i][1], units_i[i][0])
    for i in range(0, len(outputs)):
        if units_o[i] == 'None':
            s += "\t\tself.add_output('{}')\n".format(outputs[i][1])
        else:
            s += "\t\tself.add_output('{}', units='{}')\n".format(outputs[i][1], units_o[i])
    s += "\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n\n"
    s += "\tdef compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):\n"
    s += "\n" + indent(comp_f, prefix="\t\t") + "\n"
    return s
