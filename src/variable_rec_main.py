import variable_recognition as vr

TEXT = "x = y3**2.5+4e-10 #[m]\n" \
       "b = Dext/(Dalpha*1.0e-1 + 1) #[kg]\n" \
       "force = np.log(np.cos(lift + 1.3e+4)+sin(np.log(np.exp(x)) + 1\n" \
       "if area == 3e+3:\n" \
       "    elif j_2 < 3:\n" \
       "        j_2 += 1.1e + 2\n"


def main():
    inp, out, units = vr.get_variables(TEXT)
    inputs = []
    outputs = []
    print("Inputs detected:")
    print(inp)
    print("Outputs detected:")
    print(out)
    print("Units detected:")
    print(units)
    for x in inp:
        in_name = input("input name for {}:".format(x[0]))
        inputs.append([x, in_name])
    for x in out:
        out_name = input("output name for {}:".format(x[0]))
        outputs.append([x, out_name])
    text = TEXT
    print("--edited function--")
    print(vr.edit_function(inputs, outputs, text))


if __name__ == '__main__':
    main()
