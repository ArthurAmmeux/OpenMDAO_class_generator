from component_filegen import gen_file


def main():
    print("This program will generate a file")
    f_name = input("File name (without extension) :")
    name = input("Component name :")
    print("\nInputs definition :")
    inputs = []
    outputs = []
    yn = "Y"
    while yn == "Y":
        inputs.append(input("Input name :"))
        yn = input("new input ?(Y/N)")
    print("Outputs definition :")
    yn = "Y"
    while yn == "Y":
        outputs.append(input("Output name :"))
        yn = input("new output ?(Y/N)")
    print("--- Code ---\n")
    print("Computation function definition :")
    comp_f = input("Your computation function :")
    gen_file(f_name, name, inputs, outputs, comp_f)


if __name__ == main():
    main()
