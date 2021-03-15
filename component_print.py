def print_code(c_name, inputs, outputs, comp_f):
    print("class", c_name, "(om.ExplicitComponent):\n")
    print("\tdef setup(self):")
    for i in range(0, len(inputs)):
        print("\t\tself.add_input('{}')".format(inputs[i]))
    for i in range(0, len(outputs)):
        print("\t\tself.add_output('{}')".format(outputs[i]))
    print("\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n")
    print("\tdef compute(self, inputs, outputs):")
    print("\n\t\t{}".format(comp_f))
