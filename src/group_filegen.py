from textwrap import indent


def gen_group_file(f_name, g_name, subsystems, init):
    f = open("{}.py".format(f_name), "x")
    f.write("import openmdao.api as om\n")
    for i in range(len(subsystems)):
        f.write("from {} import {}\n".format(subsystems[i][2], subsystems[i][1]))
    f.write("\n\nclass {}(om.Group):\n\n".format(g_name))
    if init != 0:
        f.write("\tdef initialize(self):\n")
        f.write(indent(init, prefix="\t\t"))
        f.write("\n\n")
    f.write("\tdef setup(self):\n")
    for i in range(len(subsystems)):
        f.write('\t\tself.add_subsystem("{}", {}, promotes=["*"])\n'.format(subsystems[i][0], subsystems[i][1]))
