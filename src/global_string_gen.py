from group_parse import parse_group
from component_parse import parse_comp
from variable_recognition import get_variables, edit_function
from group_string import group_str
from component_string import component_str, component_str_derivative
from higher_parse import parse_higher
import parse_pack as pp


class CompData:
    """
    A class to store data about components
    """
    def __init__(self):
        self.group = "None"
        self.name = "DefaultName"
        self.equation = "default_ = default + 1"
        self.var_in = []
        self.var_out = []


class HGdata:
    """
    a class to store data about higher groups
    """
    def __init__(self):
        self.name = "Default_name"
        self.children = []
        self.last = False

    def child_app(self, children):
        self.children.append(children)


def is_group(str):
    """
    :param str: input string to be tested
    :return: True if the string contains a group
    """
    if "## " in str:
        return True
    return False


def total_parse(str, pack):
    """
    :param pack: list of packages that the user wants to import (instances of the Pack class)
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
                comp_data.var_in, comp_data.var_out = get_variables(c[1], pack)
                comp_data.equation = c[1]
                list_of_components.append(comp_data)

            result.append([g_name, list_of_components])
    else:
        comp = parse_comp(str)
        list_of_components = []

        for c in comp:
            comp_data = CompData()
            comp_data.name = c[0]
            comp_data.var_in, comp_data.var_out = get_variables(c[1], pack)
            comp_data.equation = c[1]
            list_of_components.append(comp_data)

        result = [["None", list_of_components]]

    return result


def is_higher_group(str):
    if '### ' in str:
        return True
    return False


def recursive_parse(str, pack, name="Default_name"):
    """
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param str: string to be parsed
    :param name: name of the higher group
    :return: a recursive data structure HGdata
    """
    if is_higher_group(str):
        hgr = parse_higher(str)
        hg_data = HGdata()
        hg_data.name = name
        for i in range(len(hgr)):
            hg_data.child_app(recursive_parse(hgr[i][1], pack, hgr[i][0]))
    else:
        hg_data = HGdata()
        hg_data.name = name
        hg_data.last = True
        hg_data.children = total_parse(str, pack)
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
            result += aggregate_result(child)
        return result


def gen_string(result, pack, d_check, imports=False):
    """
    :param imports: boolean to specify if imports are required
    :param pack: list of packages that the user wants to import (instances of the Pack class)
    :param result: a list of group names associated with their list_of_components containing CompData instances
    :param d_check: boolean to specify if derivatives are to be analytic
    :return: a string with groups and their associated components as om.Groups and om.Components
    """
    s = ""
    if result[0][0] == "None" and len(result) == 1:
        comp = result[0][1]
        if len(pack) > 0:
            s += pp.string_pack(pack)
        for i in range(len(comp)):
            s += "\n"
            comp_f = comp[i].equation
            var_in, var_out = comp[i].var_in, comp[i].var_out
            comp_f = edit_function(var_in, var_out, comp_f)
            c_name = comp[i].name
            if d_check:
                s += component_str_derivative(c_name, var_in, var_out, comp_f, pack)
            else:
                s += component_str(c_name, var_in, var_out, comp_f)
    else:
        for i in range(len(result)):
            c_data = [[comp_data.name, comp_data.name] for comp_data in result[i][1]]
            s += group_str(result[i][0], c_data, 0, pack, imports=imports)
            s += "\n"
            for comp_data in result[i][1]:
                s += "\n"
                inputs = comp_data.var_in
                outputs = comp_data.var_out
                comp_f = edit_function(inputs, outputs, comp_data.equation)
                if d_check:
                    s += component_str_derivative(comp_data.name, inputs, outputs, comp_f, pack)
                else:
                    s += component_str(comp_data.name, inputs, outputs, comp_f)
            s += "\n"
    return s


def rec_gen_string(hg_data, pack, d_check):
    """
    :param hg_data: higher group data to generate a string from
    :param pack: list of packages that the user wants to import
    :param d_check: boolean to specify if derivatives are to be analytic
    :return: generated string
    """
    s = ""
    if hg_data.last:
        names = [[hg_data.children[i][0], hg_data.children[i][0]] for i in range(len(hg_data.children))]
        s += group_str(hg_data.name, names, 0, pack) + "\n"
        s += gen_string(hg_data.children, pack, d_check)
    else:
        names = [[hg_data.children[i].name, hg_data.children[i].name] for i in range(len(hg_data.children))]
        s += group_str(hg_data.name, names, 0, pack) + "\n"
        for child in hg_data.children:
            s += rec_gen_string(child, pack, d_check)
    return s + "\n"


def multi_rec_gen_string(hg_data, pack, d_check):
    """
    :param hg_data: higher group data to generate a string from
    :param pack: list of packages that the user wants to import
    :param d_check: boolean to specify if derivatives are to be analytic
    :return: generated string (same function as the previous one but usable on multiple highest level groups)
    """
    s = ""
    if not hg_data.last:
        for child in hg_data.children:
            s += "# ---New High Level Group---\n\n"
            s += "import openmdao.api as om\n"
            if len(pack) > 0:
                s += pp.string_pack(pack)
            s += "\n"
            s += rec_gen_string(child, pack, d_check)
            s += "# ---End of High Level Group---\n"
    else:
        s += gen_string(hg_data.children, pack, d_check, imports=True)
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
        "y = z+1\n" \
        "#### HHG2\n" \
        "### HG3\n" \
        "## G3\n" \
        "# C1\n" \
        "y = x+1\n"


def main():
    # print(aggregate_result(recursive_parse(TEXT2)))
    print(multi_rec_gen_string(recursive_parse(TEXT2, pack=[]), [], True))


if __name__ == '__main__':
    main()
