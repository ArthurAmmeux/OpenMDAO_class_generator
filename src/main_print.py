from src_project.component_print import print_code


def main():
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
    print_code(name, inputs, outputs, comp_f)


if __name__ == '__main__':
    main()
