from textwrap import indent


def print_code(c_name, inputs, outputs, units_i, units_o, comp_f):
    """
    :param c_name: component name
    :param inputs: list of input variables "renamed"
    :param outputs: list of output variables "renamed"
    :param comp_f: edited computation function
    :return: prints the code of an om.Component
    """
    print("class", c_name, "(om.ExplicitComponent):\n")
    print("\tdef setup(self):")
    for i in range(0, len(inputs)):
        if units_i[i][0] == 'None':
            print("\t\tself.add_input('{}', val={})".format(inputs[i][1], units_i[i][1]))
        else:
            print("\t\tself.add_input('{}', val={}, units='{}')".format(inputs[i][1], units_i[i][1], units_i[i][0]))
    for i in range(0, len(outputs)):
        if units_o[i] == 'None':
            print("\t\tself.add_output('{}')".format(outputs[i][1]))
        else:
            print("\t\tself.add_output('{}', units='{}')".format(outputs[i][1], units_o[i]))
    print("\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n")
    print("\tdef compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):")
    print("\n" + indent(comp_f, prefix="\t\t"))
