from textwrap import indent


def print_code(c_name, inputs, outputs, comp_f):
    print("import numpy as np\nimport openmdao.api as om\n")
    print("class", c_name, "(om.ExplicitComponent):\n")
    print("\tdef setup(self):")
    for i in range(0, len(inputs)):
        print("\t\tself.add_input('{}', val=np.nan)".format(inputs[i]))
    for i in range(0, len(outputs)):
        print("\t\tself.add_output('{}', val=np.nan)".format(outputs[i]))
    print("\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n")
    print("\tdef compute(self, inputs, outputs):")
    print("\n" + indent(comp_f, prefix="\t\t") + "\n")
