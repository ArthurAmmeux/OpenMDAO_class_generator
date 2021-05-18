from component_print import print_code
from component_parse import parse_comp
from variable_recognition import get_variables, edit_function


def print_components(str):

    """
    :param str: input string that is to be parsed
    :return: prints the components found in the input string as om.Components
    """

    comp = parse_comp(str)
    for i in range(len(comp)):
        print("---New Component---\n")
        comp_f = comp[i][1]
        var_in, var_out = get_variables(comp_f)
        inputs = [[x, x + '_name'] for x in var_in]
        outputs = [[x, x + '_name'] for x in var_out]
        comp_f = edit_function(inputs, outputs, comp_f)
        c_name = comp[i][0]
        print_code(c_name, [x + '_name' for x in var_in], [x + '_name' for x in var_out], comp_f)
        print("---End of Component---\n")


TEXT = "# FistComponent\n" \
       "x = y + 1\n" \
       "z = y**2 + x\n" \
       "w = v + np.sin(a)\n" \
       "" \
       "# SecondComponent\n" \
       "a = np.log(b + 3*c)\n" \
       "d = c**2 + 3* b-1\n" \
       "e = h**3 + 2\n" \
       ""


def main():
    print_components(TEXT)


if __name__ == '__main__':
    main()
