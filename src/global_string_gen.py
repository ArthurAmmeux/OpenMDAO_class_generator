from group_parse import parse_group
from component_parse import parse_comp
from variable_recognition import get_variables, edit_function
from group_string import group_str
from component_string import component_str
from higher_parse import parse_higher


class CompData:
    """
    A class to store data about components
    """
    group = "None"
    name = "DefaultName"
    equation = "default_ = default + 1"
    var_in = []
    var_out = []
    units_i = []
    units_o = []


class HGdata:
    """
    a class to store data about higher groups
    """
    name = "Default_name"
    children = []
    last = False


def is_group(str):
    """
    :param str: input string to be tested
    :return: True if the string contains a group
    """
    if "## " in str:
        return True
    return False


def total_parse(str):
    """
    :param str: input string to be parsed
    :return: result is a list of group names associated with their list_of_components containing CompData instances
    """
    result = []

    if is_group(str):
        groups = parse_group(str)

        for g in groups:
            g_name = g[0]
            comp = parse_comp(g[1])
            list_of_components = []

            for c in comp:
                comp_data = CompData()
                comp_data.group = g[0]
                comp_data.name = c[0]
                comp_data.var_in, comp_data.var_out, comp_data.units_o = get_variables(c[1])
                comp_data.units_i = [['None', 'np.nan'] for i in range(len(comp_data.var_in))]
                # comp_data.units_o = ['None'] * len(comp_data.var_out)
                comp_data.equation = c[1]
                list_of_components.append(comp_data)

            result.append([g_name, list_of_components])
    else:
        comp = parse_comp(str)
        list_of_components = []

        for c in comp:
            comp_data = CompData()
            comp_data.name = c[0]
            comp_data.var_in, comp_data.var_out, comp_data.units_o = get_variables(c[1])
            comp_data.units_i = [['None', 'np.nan'] for i in range(len(comp_data.var_in))]
            # comp_data.units_o = ['None'] * len(comp_data.var_out)
            comp_data.equation = c[1]
            list_of_components.append(comp_data)

        result = [["None", list_of_components]]

    return result


def is_higher_group(str):
    if '### ' in str:
        return True
    return False


def recursive_parse(str, name="Default_name"):
    """
    :param str: string to be parsed
    :param name: name of the higher group
    :return: a recursive data structure HGdata
    """
    if is_higher_group(str):
        hgr = parse_higher(str)
        hg_data = HGdata()
        hg_data.name = name
        print(hgr)
        for i in range(len(hgr)):
            print("for", i)
            hg_data.children.append(recursive_parse(hgr[i][1], hgr[i][0]))
            print(hg_data.children[i].name)
            print(len(hg_data.children))
        print(len(hg_data.children))
        print("endfor", i)
    else:
        print("groups")
        hg_data = HGdata()
        hg_data.name = name
        hg_data.last = True
        hg_data.children = total_parse(str)
    return hg_data


def aggregate_result(hg_data):
    """
    :param hg_data: higher group data to be aggregated
    :return: a global result with all groups, components and variables
    """
    if hg_data.last:
        return hg_data.children
    else:
        result = []
        for child in hg_data.children:
            result.append(aggregate_result(child))
        return result


def gen_string(result, np=False):
    """
    :param np: boolean to specify if the user wants to import numpy
    :param result: a list of group names associated with their list_of_components containing CompData instances
    :return: a string with groups and their associated components as om.Groups and om.Components
    """
    s = ""
    if result[0][0] == "None" and len(result) == 1:
        comp = result[0][1]
        s += "import openmdao.api as om\n"
        if np:
            s += "import numpy as np\n"
        s += "\n"
        for i in range(len(comp)):
            s += "\n"
            comp_f = comp[i].equation
            var_in, var_out = comp[i].var_in, comp[i].var_out
            comp_f = edit_function(var_in, var_out, comp_f)
            c_name = comp[i].name
            s += component_str(c_name, var_in, var_out, comp[i].units_i, comp[i].units_o, comp_f)
    else:
        for i in range(len(result)):
            s += "# ---New Group---\n\n"
            c_data = [[comp_data.name, comp_data.name, comp_data.name + "_pack"] for comp_data in result[i][1]]
            s += group_str(result[i][0], c_data, 0, np)
            s += "\n"
            for comp_data in result[i][1]:
                s += "\n"
                inputs = comp_data.var_in
                outputs = comp_data.var_out
                comp_f = edit_function(inputs, outputs, comp_data.equation)
                s += component_str(comp_data.name, inputs, outputs, comp_data.units_i, comp_data.units_o, comp_f)
            s += "# ---End of Group---\n"
    return s


TEXT = "\n" \
       "## Group1\n" \
       "# Component1\n" \
       "\n" \
       "\n" \
       "x = y*3 +2\n" \
       "z = w**2 +a*4\n" \
       "\n" \
       "# Component2\n" \
       "a = b_/(c_ + c**2)\n" \
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

TEXT2 = "\n" \
        "#### HHG1\n" \
        "### HG1\n" \
        "## G1\n" \
        "# C1\n" \
        "y = x+1\n" \
        "### HG2\n" \
        "## G2\n" \
        "# C2\n" \
        "y = x+1\n"


def main():
    # print(gen_string(total_parse(TEXT), True))
    print(recursive_parse(TEXT2))
    # print(aggregate_result(recursive_parse(TEXT2)))


if __name__ == '__main__':
    main()
