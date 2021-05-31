from textwrap import indent
from variable_recognition import edit_function
import global_string_gen as gs
import os


def open_file(f_name):
    """
    :param f_name: name of the file
    :return: a new file with as many (1) as needed to not already exist
    """
    try:
        f = open("{}.py".format(f_name), "x")
        return f
    except IOError:
        return open_file(f_name + "(1)")


def generate_file(result, np=False):
    """
    :param np: boolean to specify if the user wants to import numpy
    :param result: a list of group names associated with their list_of_components containing CompData instances
    :return: generates one file per group with python code
    """
    if result[0][0] == "None" and len(result) == 1:
        comp = result[0][1]
        f_name = comp[0].name
        f = open_file(f_name)
        f.write("import openmdao.api as om\n")
        if np:
            f.write("import numpy as np\n")
        f.write("\n\n")
        for i in range(len(comp)):
            comp_f = comp[i].equation
            var_in, var_out = comp[i].var_in, comp[i].var_out
            units_i = comp[i].units_i
            units_o = comp[i].units_o
            comp_f = edit_function(var_in, var_out, comp_f)
            c_name = comp[i].name
            add_component(f, c_name, var_in, var_out, units_i, units_o, comp_f)
        f.close()
        os.system("black " + f_name + ".py")
    else:
        for i in range(len(result)):
            f_name = result[i][0]
            f = open_file(f_name)
            f.write("import openmdao.api as om\n")
            if np:
                f.write("import numpy as np\n")
            f.write("\n\n")
            add_group(f, result[i][0], [[comp.name, comp.name]for comp in result[i][1]], 0)
            for comp_data in result[i][1]:
                comp_f = comp_data.equation
                var_in, var_out = comp_data.var_in, comp_data.var_out
                units_i = comp_data.units_i
                units_o = comp_data.units_o
                comp_f = edit_function(var_in, var_out, comp_f)
                c_name = comp_data.name
                add_component(f, c_name, var_in, var_out, units_i, units_o, comp_f)
            f.close()
            os.system("black " + f_name + ".py")


def new_generate_file(hg_data, np=False):
    """
    :param hg_data: input parsed data as Hg_data
    :param np: boolean to specify if numpy is to be imported
    :return: generates as many files as there are highest level groups
    """
    if hg_data.last:
        generate_file(hg_data.children, np=np)
    else:
        for child in hg_data.children:
            s = gs.rec_gen_string(child, np=np)
            f_name = child.name
            f = open_file(f_name)
            f.write("import openmdao.api as om\n")
            if np:
                f.write("import numpy as np\n")
            f.write("\n\n")
            f.write(s)
            f.close()
            os.system("black " + f_name + ".py")


def add_component(f, c_name, inputs, outputs, units_i, units_o, comp_f):
    """
    :param f: target file
    :param c_name: component name
    :param inputs: list of input variables and their associated names
    :param outputs: list of output variables and their associated names
    :param units_i: list of input variable units and default values
    :param units_o: list of output variable units and default values
    :param comp_f: edited computation function
    :return: writes in the target file the code for the selected component
    """

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
    """
    :param f: target file
    :param g_name: group name
    :param subsystems: list of names of the components of the group
    :param init: initialization function if needed
    :return: writes in the target file the code for the selected group (without the code for the components)
    """

    f.write("class {}(om.Group):\n\n".format(g_name))
    if init != 0:
        f.write("\tdef initialize(self):\n")
        f.write(indent(init, prefix="\t\t"))
        f.write("\n\n")
    f.write("\tdef setup(self):\n")
    for i in range(len(subsystems)):
        f.write('\t\tself.add_subsystem("{}", {}, promotes=["*"])\n'.format(subsystems[i][0], subsystems[i][1]))
    f.write("\n\n")
