from textwrap import indent


def print_group(g_name, subsystems, init):
    print("import openmdao.api as om")
    for i in range(len(subsystems)):
        print("from {} import {}".format(subsystems[i][2], subsystems[i][1]))
    print("\n")
    print("class {}(om.Group):\n".format(g_name))
    if init != 0:
        print("\tdef initialize(self):")
        print(indent(init, prefix="\t\t"))
        print("")
    print("\tdef setup(self):")
    for i in range(len(subsystems)):
        print('\t\tself.add_subsystem("{}", {}, promotes=["*"])'.format(subsystems[i][0], subsystems[i][1]))
