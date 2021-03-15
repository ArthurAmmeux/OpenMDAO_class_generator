def gen_file(f_name, c_name, inputs, outputs, units_i, units_o, comp_f):
    f = open("{}.py".format(f_name), "x")
    f.write("import numpy as np\nimport openmdao.api as om\n\n\n")
    f.write("class {}(om.ExplicitComponent):\n".format(c_name))
    f.write("\n\tdef setup(self):")
    for i in range(0, len(inputs)):
        if units_i[i][0]:
            f.write('\n\t\tself.add_input("{}", val=np.nan)'.format(inputs[i]))
        else:
            f.write('\n\t\tself.add_input("{}", val=np.nan, units="{}")'.format(inputs[i], units_i[i][1]))
    for i in range(0, len(outputs)):
        if units_o[i][0]:
            f.write('\n\t\tself.add_output("{}", val=np.nan)'.format(outputs[i]))
        else:
            f.write('\n\t\tself.add_output("{}", val=np.nan, units="{}")'.format(outputs[i], units_o[i][1]))
    f.write("\n\n\tdef setup_partials(self):\n\t\tself.declare_partials('*', '*', method='fd')\n")
    f.write("\n\tdef compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):")
    f.write("\n\t\t{}\n".format(comp_f))
