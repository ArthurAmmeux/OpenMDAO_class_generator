from textwrap import indent


def group_str(g_name, subsystems, init, np=False):
    """
    :param np: boolean to specify if the user wants to import numpy
    :param g_name: group name
    :param subsystems: list of the components that are to be added to the group
    (component name, class name, package name)
    :param init: content of the initialization function, 0 if no function is required
    :return: a string containing the code of an om.Group
    """
    s = ""
    s += "import openmdao.api as om\n"
    if np:
        s += "import numpy as np\n"
    s += "\n\nclass {}(om.Group):\n\n".format(g_name)
    if init != 0:
        s += "\tdef initialize(self):\n\n"
        s += indent(init, prefix="\t\t")
        s += "\n"
    s += "\tdef setup(self):\n"
    for i in range(len(subsystems)):
        s += '\t\tself.add_subsystem("{}", {}, promotes=["*"])\n'.format(subsystems[i][0], subsystems[i][1])
    return s
