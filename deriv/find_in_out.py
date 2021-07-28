def find_in_out(lines):
    """
    :param lines: a list of lines of the compute() function
    :return: a tuple consisting of two dictionaries with the detected inputs and outputs from the initialization part of
    the function
    """
    inputs = {}
    outputs = {}
    for line in lines:
        if "inputs[" in line:
            eq = line.split("=")
            sym = eq[0].strip()
            inp = eq[1].replace("inputs[", "")
            inp = inp.replace("]", "")
            inp = inp.strip()
            inp = inp[1:-1]
            inputs[sym] = inp
        if "outputs[" in line:
            eq = line.split("=")
            sym = eq[1].strip()
            out = eq[0].replace("outputs[", "")
            out = out.replace("]", "")
            out = out.strip()
            out = out[1:-1]
            outputs[sym] = out
    return inputs, outputs


def update_variables(inputs, outputs, f_inputs, f_outputs):
    """
    :param inputs: inputs found in the equations
    :param outputs: outputs found in the equations
    :param f_inputs: inputs found in compute() initialization
    :param f_outputs: inputs found in compute() initialization
    :return: modifies inputs and outputs to delete variables not declared in the original file
    """
    for inp in inputs:
        inter = True
        for fi in f_inputs:
            if inp.symbol == fi:
                inp.name = f_inputs[fi]
                inter = False
        if inter:
            inputs.remove(inp)
    for out in outputs:
        inter = True
        for fo in f_outputs:
            if out.symbol == fo:
                out.name = f_outputs[fo]
                inter = False
        if inter:
            outputs.remove(out)


EQ = '        a = inputs["a_name"]\n'\
    '       b = inputs["b_name"]\n'\
    '       x = inputs["x_name"]\n'\
    '       y = inputs["y_name"]\n\n'\
    '       long_variable = a + b\n'\
    '       function_test = np.log(x + np.sin(y))  # [rad]\n\n'\
    '       outputs["long_variable_name"] = long_variable\n'\
    '       outputs["function_test_name"] = function_test'


def main():
    inputs, outputs = find_in_out(EQ.splitlines())
    print(inputs)
    print(outputs)


if __name__ == '__main__':
    main()
