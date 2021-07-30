import threading
import variable_recognition as vr
import parse_pack as pp
import derivative_string as ds
import argparse as ap
import find_in_out as fio
import loading as ld
import handle_method as hm
import os
import re
import time


def open_file(f_name):
    """
    :param f_name: name of the file
    :return: a new file with as many (1) as needed to not already exist
    """
    try:
        f = open("{}.py".format(f_name), "x")
        return f
    except IOError:
        return open_file(f_name + "(1)")


def modify_str(str, comp_naming):
    """
    :param str: input string
    :param comp_naming: name of the ExplicitComponent class in this file (with or without om.)
    :return: the modified string with analytic derivatives
    """
    pa = str.split("class", 1)[0]
    pack = pp.parse_pack(pa)
    comp = str.split(comp_naming)
    f_str = comp[0]
    for index in range(1, len(comp)):
        spt_comp = comp[index].splitlines()
        c_lines, last = spt_comp[:-1], spt_comp[-1]
        ct = ""
        for s in c_lines:
            ct += s + "\n"
        cf = ct.split("def compute(")
        fc = cf[1].split(" def ", 1)
        func = fc[0]
        lines = func.splitlines()[1:]
        if index == len(comp) - 1:
            lines.append(last)
        f_inputs, f_outputs = fio.find_in_out(lines)
        i1 = 0
        for i in range(len(lines)):
            if lines[i].strip() != "" and "inputs[" not in lines[i]:
                i1 = i
                break
        i2 = i1
        for j in range(i1, len(lines)):
            if "outputs[" in lines[j]:
                i2 = j
                break
        equations = ""
        for i in range(i1, i2):
            equations += lines[i] + "\n"

        method_calls_iter = re.finditer(r'self.\w+\([\w, (/*+-]*\)', equations)
        method_calls = []
        for match in method_calls_iter:
            op = match[0].count("(")
            cl = match[0].count(")")
            index_m = match.end()
            method_call = match[0]
            while op != cl:
                method_call += equations[index_m]
                op = method_call.count("(")
                cl = method_call.count(")")
                index_m += 1
            method_calls.append(method_call)
        while method_calls:
            equations = hm.handle_method(method_calls, equations, str, pack)
            method_calls_iter = re.finditer(r'self.\w+\([\w, (/*+-]*\)', equations)
            method_calls = []
            for match in method_calls_iter:
                op = match[0].count("(")
                cl = match[0].count(")")
                index_m = match.end()
                method_call = match[0]
                while op != cl:
                    method_call += equations[index_m]
                    op = method_call.count("(")
                    cl = method_call.count(")")
                    index_m += 1
                method_calls.append(method_call)

        inputs, outputs, const = vr.get_variables(equations, pack)
        fio.update_variables(inputs, outputs, f_inputs, f_outputs)
        ls = ds.derivative_str(inputs, outputs, const, pack)

        if index == len(comp) - 1:
            ct += last

        if "def setup_partials" in ct:
            set1 = ct.split("setup_partials(self):")
            set2 = set1[1].split("def ", 1)
            new_str = set1[0]
            new_str += ls[0]
            new_str += "\n    def "
            new_str += set2[1]
            new_str = new_str.strip()
            new_str += "\n\n" + ls[1]
        else:
            ct = ct.replace('self.declare_partials("*", "*", method="fd")', "")
            set1 = ct.split("def compute")
            new_str = set1[0].strip()
            new_str += "\n\n    def " + ls[0]
            new_str += "\n    def compute"
            new_str += set1[1]
            new_str = new_str.strip()
            new_str += "\n\n" + ls[1]

        f_str += comp_naming + new_str
        if index == len(comp) - 1:
            f_str += "\n"
        else:
            f_str += "\n" + last
    return f_str


def check_derivatives(f_str, comp_naming, exc):
    """
    :param f_str: output string of modify_str
    :param comp_naming: name of the ExplicitComponent class in this file (with or without om.)
    :return: checks if the generated derivatives are close to the numerical ones
    """
    data = {}
    f_str = f_str.replace("val=np.nan", "val=0")
    spt = f_str.split(comp_naming)
    comps = spt[:-1]
    for i in range(len(comps)):
        comps[i] = comps[i].splitlines()[-1]
        comps[i] = comps[i].replace("class", "")
        comps[i] = comps[i].strip()
    f_str += "\n\nproblem = om.Problem()\n"

    for comp in comps:
        f_str += "problem.model.add_subsystem('{}', {}())\n".format(comp, comp)

    f_str += "problem.set_solver_print(level=0)\n"\
        "problem.setup()\n"\
        "problem.run_model()\n"\
        "data = problem.check_partials()\n"
    exec(f_str)
    for comp in data:
        for key in data[comp]:
            fwd = data[comp][key][0]
            if fwd > 1e-3:
                exc[1] = 1


def add_derivative(file_name, m_name, exc, dir, check, outfile="", outdir=""):
    """
    :param file_name: name of the .py file to add analytic derivatives to
    :param m_name: list of one element to retrieve created file name
    :param exc: list of 2 elements to retrieve error data
    :param dir: boolean to specify if the function is applied to a directory or a single file
    :param check: boolean to specify if the generated derivatives are to checked
    :param outfile: name of the output file
    :param outdir: name of the output directory
    :return: generates a new .py file with the analytic derivatives added
    """
    f = open(file_name)
    str = f.read()

    if "(om.ExplicitComponent)" in str and "compute_partials(" not in str:
        try:
            f_str = modify_str(str, "(om.ExplicitComponent)")
        except Exception:
            exc[0] = True
            exit()
            f_str = None
        if check:
            check_derivatives(f_str, "(om.ExplicitComponent)", exc)
    elif "(ExplicitComponent)" in str and "compute_partials(" not in str:
        try:
            f_str = modify_str(str, "(ExplicitComponent)")
        except Exception:
            exc[0] = True
            exit()
            f_str = None
        if check:
            check_derivatives(f_str, "(ExplicitComponent)", exc)
    else:
        exc[0] = True
        exit()
        f_str = None

    if outfile:
        f_ = open_file(outfile)
        f_.write(f_str)
        f.close()
        f_.close()
        m_name[0] = f_.name
    elif dir:
        if outdir:
            if not os.path.isdir("../" + outdir):
                os.mkdir("../" + outdir)
            f_ = open_file("../" + outdir + "/" + file_name[:-3])
        else:
            default_dir = "d_" + os.getcwd().split("\\")[-1]
            if not os.path.isdir("../" + default_dir):
                os.mkdir("../" + default_dir)
            f_ = open_file("../" + default_dir + "/" + file_name[:-3])
        f_.write(f_str)
        f.close()
        f_.close()
        m_name[0] = f_.name
    else:
        f_ = open_file(file_name[:-3] + "_d")
        f_.write(f_str)
        f.close()
        f_.close()
        m_name[0] = f_.name


def main():
    parser = ap.ArgumentParser(description="adds analytic derivative to an om.Component python file")
    parser.add_argument('-dir', type=bool, default=False,
                        help="if True, applies add_derivative to the chosen directory instead of a file")
    parser.add_argument('file', type=str, help=".py file or directory to add analytic derivatives to")
    parser.add_argument('-outfile', type=str,
                        help="name of the generated file (without extension)")
    parser.add_argument('-outdir', type=str,
                        help="name of the generated directory")
    parser.add_argument('-check', type=bool, default=False, help="if True checks the generated analytic derivatives")
    arg = parser.parse_args()
    directory = vars(arg)['dir']
    fd_name = vars(arg)['file']
    outfile = vars(arg)['outfile']
    outdir = vars(arg)['outdir']
    check = vars(arg)['check']
    if directory:
        os.chdir("./" + fd_name)
        files = os.listdir()
        for file in files:
            m_name = [""]
            exc = [False, False]
            process = threading.Thread(target=add_derivative, args=(file, m_name, exc, True, check, "", outdir))
            process.start()
            ld.loading(process)
            if exc[0]:
                print("\r!!! Unable to process the file " + file + " !!!", flush=True)

            elif exc[1]:
                print("\r!!! Generated derivatives too far from numerical ones in" + file + "in" + m_name[0] + "!!!",
                      flush=True)

            else:
                print("\r*** Derivatives successfully added to " + file + " in " + m_name[0] + " ***", flush=True)
    else:
        m_name = [""]
        exc = [False, False]
        if outfile:
            process = threading.Thread(target=add_derivative, args=(fd_name, m_name, exc, False, check, outfile))
            process.start()
            ld.loading(process)
        else:
            process = threading.Thread(target=add_derivative, args=(fd_name, m_name, exc, False, check))
            process.start()
            ld.loading(process)
        if exc[0]:
            print("\r!!! Unable to process the file " + fd_name + " !!!", flush=True)

        elif exc[1]:
            print("\r!!! Generated derivatives too far from numerical ones in" + fd_name + "!!!",
                  flush=True)
        else:
            print("\r*** Derivatives successfully added to " + fd_name + " in " + m_name[0] + " ***", flush=True)


if __name__ == '__main__':
    main()
