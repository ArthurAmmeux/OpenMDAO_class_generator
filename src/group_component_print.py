from group_parse import parse_group
from component_parse import parse_comp
from variable_recognition import get_variables, edit_function
from group_print import print_group
from component_print import print_code


class CompData:
    name = "DefaultName"
    equation = "y = x + 1 ### default equation"
    var_in = []
    var_out = []


def total_parse(str):
    groups = parse_group(str)
    result = []

    for g in groups:
        g_name = g[0]
        comp = parse_comp(g[1])
        list_of_components = []

        for c in comp:
            comp_data = CompData()
            comp_data.name = c[0]
            comp_data.var_in, comp_data.var_out = get_variables(c[1])
            comp_data.equation = c[1]
            list_of_components.append(comp_data)

        result.append([g_name, list_of_components])

    return result


def print_all(result):
    print("---New code---\n")
    for i in range(len(result)):
        print("---New Group---\n")
        print_group(result[i][0], [[comp_data.name + "_name", comp_data.name, comp_data.name + "_pack"] for comp_data in result[i][1]], 0)
        print("\n")
        for comp_data in result[i][1]:
            print("---New Component---\n")
            inputs = [[x, x + "_name"] for x in comp_data.var_in]
            outputs = [[x, x + "_name"] for x in comp_data.var_out]
            comp_f = edit_function(inputs, outputs, comp_data.equation)
            print_code(comp_data.name, inputs, outputs, comp_f)
            print("---End of Component---\n")
        print("---End of Group---")


TEXT = "\n" \
       "## Group1\n" \
       "# Component1\n" \
       "\n" \
       "\n" \
       "x = y*3 +2\n" \
       "z = w**2 +a*4\n" \
       "\n" \
       "# Component2\n" \
       "a = b + c*2\n" \
       "d = e + f\n" \
       "## Group2\n" \
       "\n" \
       "\n" \
       "# Component3\n" \
       "\n" \
       "\n" \
       "x = y*3 +5\n" \
       "z = w**2 +a*3\n" \
       "\n" \
       "# Component4\n" \
       "a = b + c*6\n" \
       "d = e + f*3\n" \
       "\n"


def main():
    print_all(total_parse(TEXT))


if __name__ == '__main__':
    main()
