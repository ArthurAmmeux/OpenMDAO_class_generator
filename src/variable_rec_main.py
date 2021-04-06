import variable_recognition as vr

TEXT = "x = y3**2+z4 * 3 -6*area\n" \
       "b = z4**4 + 3%c_ -area/2\n" \
       "force = np.log(np.cos(lift)+sin(np.log(np.exp(x)) + 1\n1" \
       "if area == 3:\n" \
       "    elif j_2 < 3:\n" \
       "        j_2 += 1\n" \


def main():
    inp, out = vr.get_variables(TEXT)
    inputs = []
    outputs = []
    print("Inputs detected:")
    print(inp)
    print("Outputs detected:")
    print(out)
    for x in inp:
        in_name = input("input name for {}:".format(x))
        inputs.append([x, in_name])
    for x in out:
        out_name = input("output name for {}:".format(x))
        outputs.append([x, out_name])
    text = TEXT
    print("--edited function--")
    print(vr.edit_function(inputs, outputs, text))


if __name__ == '__main__':
    main()
