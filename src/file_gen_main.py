from src_project.component_filegen import gen_file


def main():
    print("This program will generate a file")
    f_name = input("File name (without extension) :")
    name = input("Component name :")
    print("\nInputs definition :")
    inputs = []
    outputs = []
    units_i = []
    units_o = []
    yn = "Y"
    while yn == "Y":
        inputs.append(input("Input name :"))
        yn = input("Specify unit ?(Y/N)")
        if yn == "Y":
            units_i.append([0, input("Unit name :")])
        else:
            units_i.append([1, 0])
        yn = input("New input ?(Y/N)")
    print("Outputs definition :")
    yn = "Y"
    while yn == "Y":
        outputs.append(input("Output name :"))
        yn = input("Specify unit ?(Y/N)")
        if yn == "Y":
            units_o.append([0, input("Unit name :")])
        else:
            units_o.append([1, 0])
        yn = input("New output ?(Y/N)")
    print("Computation function definition :")
    comp_f = input("Your computation function :")
    gen_file(f_name, name, inputs, outputs, units_i, units_o, comp_f)


if __name__ == main():
    main()
