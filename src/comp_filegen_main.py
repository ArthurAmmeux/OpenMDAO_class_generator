from component_filegen import gen_file
import variable_recognition as vr

comp_f = "x = y3**2+z4 * 3 -6*area\n" \
       "b = z4**4 + 3%c_ -area/2\n" \
       "force = np.log(np.cos(lift)+sin(np.log(np.exp(x)) + 1\n" \
       "if area == 3:\n" \
       "    elif j_2 < 3:\n" \
       "        j_2 += 1\n" \



def main():
    print("This program will generate a file")
    f_name = input("File name (without extension) :")
    name = input("Component name :")

    # print("Computation function definition :")
    # comp_f = input("Your computation function :")

    units_i = []
    units_o = []

    inp, out = vr.get_variables(comp_f)
    inputs = []
    outputs = []
    print("Inputs detected:")
    print(inp)
    print("Outputs detected:")
    print(out)
    for x in inp:
        in_name = input("input name for {}:".format(x))
        units_i.append([0, input("unit for {}:".format(x))])
        inputs.append([x, in_name])
    for x in out:
        out_name = input("output name for {}:".format(x))
        units_o.append([0, input("unit for {}:".format(x))])
        outputs.append([x, out_name])

    print("--edited function--")
    comp_f_edited = vr.edit_function(inputs, outputs, comp_f)
    print(comp_f_edited)

    gen_file(f_name, name, [row[1] for row in inputs], [row[1] for row in outputs], units_i, units_o, comp_f_edited)


if __name__ == '__main__':
    main()
