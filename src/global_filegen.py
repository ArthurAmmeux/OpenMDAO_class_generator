from textwrap import indent
from variable_recognition import edit_function


def generate_file(result):
    if result[0][0] == "None" and len(result) == 1:
        comp = result[0][1]
        f_name = comp[0].name
        f = open("{}.py".format(f_name), "x")
        f.write("import numpy as np\nimport openmdao.api as om\n\n\n")
        for i in range(len(comp)):
            comp_f = comp[i].equation
            var_in, var_out = comp[i].var_in, comp[i].var_out
            units_i = comp[i].units_i
            units_o = comp[i].units_o
            comp_f = edit_function(var_in, var_out, comp_f)
            c_name = comp[i].name
            add_component(f, c_name, var_in, var_out, units_i, units_o, comp_f)

    else:
        for i in range(len(result)):
            f_name = result[i][0]
            f = open("{}.py".format(f_name), "x")
            f.write("import numpy as np\nimport openmdao.api as om\n\n\n")
            add_group(f, result[i][0], [[comp.name, comp.name]for comp in result[i][1]], 0)
            for comp_data in result[i][1]:
                comp_f = comp_data.equation
                var_in, var_out = comp_data.var_in, comp_data.var_out
                units_i = comp_data.units_i
                units_o = comp_data.units_o
                comp_f = edit_function(var_in, var_out, comp_f)
                c_name = comp_data.name
                add_component(f, c_name, var_in, var_out, units_i, units_o, comp_f)


def add_component(f, c_name, inputs, outputs, units_i, units_o, comp_f):

    f.write("class {}(om.ExplicitComponent):\n".format(c_name))
    f.write("\n\tdef setup(self):")
    for i in range(0, len(inputs)):
        if units_i[i][0] == 'None':
            f.write('\n\t\tself.add_input("{}", val={})'.format(inputs[i][1], units_i[i][1]))
        else:
            f.write('\n\t\tself.add_input("{}", val={}, units="{}")'.format(inputs[i][1], units_i[i][1], units_i[i][0]))
    for i in range(0, len(outputs)):
        if units_o[i] == 'None':
            f.write('\n\t\tself.add_output("{}")'.format(outputs[i][1]))
        else:
            f.write('\n\t\tself.add_output("{}", units="{}")'.format(outputs[i][1], units_o[i]))
    f.write("\n\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n")
    f.write("\n\tdef compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):")
    f.write("\n" + indent(comp_f, prefix="\t\t") + "\n\n")


def add_group(f, g_name, subsystems, init):

    f.write("class {}(om.Group):\n\n".format(g_name))
    if init != 0:
        f.write("\tdef initialize(self):\n")
        f.write(indent(init, prefix="\t\t"))
        f.write("\n\n")
    f.write("\tdef setup(self):\n")
    for i in range(len(subsystems)):
        f.write('\t\tself.add_subsystem("{}", {}, promotes=["*"])\n'.format(subsystems[i][0], subsystems[i][1]))
    f.write("\n\n")
