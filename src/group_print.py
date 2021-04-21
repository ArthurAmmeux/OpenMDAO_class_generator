from textwrap import indent


def print_group(g_name, subsystems, init):
    """
    :param g_name: group name
    :param subsystems: list of the components that are to be added to the group
    (component name, class name, package name)
    :param init: content of the initialization function, 0 if no function is required
    :return: prints the code of an om.Group
    """
    print("import openmdao.api as om")
    print("import numpy as np\n\n")
    # for i in range(len(subsystems)):
    #   print("from {} import {}".format(subsystems[i][2], subsystems[i][1]))
    # print("\n")
    print("class {}(om.Group):\n".format(g_name))
    if init != 0:
        print("\tdef initialize(self):")
        print(indent(init, prefix="\t\t"))
        print("")
    print("\tdef setup(self):")
    for i in range(len(subsystems)):
        print('\t\tself.add_subsystem("{}", {}, promotes=["*"])'.format(subsystems[i][0], subsystems[i][1]))
