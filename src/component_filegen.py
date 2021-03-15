def gen_file(f_name, c_name, inputs, outputs, comp_f):
    f = open("{}.py".format(f_name), "x")
    f.write("class {}(om.ExplicitComponent):\n".format(c_name))
    f.write("\n\tdef setup(self):")
    for i in range(0, len(inputs)):
        f.write("\n\t\tself.add_input('{}')".format(inputs[i]))
    for i in range(0, len(outputs)):
        f.write("\n\t\tself.add_output('{}')".format(outputs[i]))
    f.write("\n\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n")
    f.write("\n\tdef compute(self, inputs, outputs):")
    f.write("\n\t\t{}".format(comp_f))
