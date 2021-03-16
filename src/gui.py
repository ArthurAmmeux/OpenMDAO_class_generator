from tkinter import *
from tkinter import ttk
from component_filegen import gen_file


root = Tk()
root.title("Fast-OAD class generator")
# root.configure(background="light grey")

f_name = "default_name"
c_name = "DefaultClassName"
inputs = []
outputs = []
units_i = []
units_o = []
comp_f = "'''function not specified'''\npass"

row_i = 0
row_o = 0

style = ttk.Style()
style.configure("Treeview")
style.theme_use("default")


def generation():
    global f_name
    global c_name
    global inputs
    global outputs
    global units_i
    global units_o
    global comp_f
    comp_f = text_box.get('1.0', END)
    print(f_name)
    print(c_name)
    print(inputs)
    print(outputs)
    print(comp_f)
    gen_file(f_name, c_name, inputs, outputs, units_i, units_o, comp_f)


def f1(event):
    global f_name
    f_name = e1.get()
    e1["bg"] = "light green"
    e2.focus_set()
    print(e1.get())


def f2(event):
    global c_name
    c_name = e2.get()
    e2["bg"] = "light green"
    e3.focus_set()
    print(e2.get())


def f3(event):
    global inputs
    inp = e3.get()
    inputs.append(inp)
    units_i.append([1, 0])
    add_input(inp)
    print(inp)
    e3.delete(0, END)


def f4(event):
    global outputs
    out = e4.get()
    outputs.append(out)
    units_o.append([1, 0])
    add_output(out)
    print(out)
    e4.delete(0, END)


lab1 = Label(root, text="File name")
lab2 = Label(root, text="Class name")
lab3 = Label(root, text="Input")
lab4 = Label(root, text="Output")
lab5 = Label(root, text="Computation Function")

e1 = Entry(root, width=40)
e2 = Entry(root, width=40)
e3 = Entry(root, width=40)
e4 = Entry(root, width=40)
text_box = Text(root, width=70, height=20)
text_box.configure(font=("Courier", 12), borderwidth = 3)

added_inputs = ttk.Treeview(root)
added_inputs["columns"] = ("Name", "default value", "units")

added_inputs.column("#0", width=0, minwidth=0)
added_inputs.column("Name", anchor=CENTER, width=120)
added_inputs.column("default value", anchor=CENTER, width=120)
added_inputs.column("units", anchor=CENTER, width=120)

added_inputs.heading("Name", text="Name")
added_inputs.heading("default value", text="default value")
added_inputs.heading("units", text="units")

added_inputs.tag_configure("even", background="white")
added_inputs.tag_configure("odd", background="light blue")


added_outputs = ttk.Treeview(root)
added_outputs["columns"] = ("Name", "default value", "units")

added_outputs.column("#0", width=0, minwidth=0)
added_outputs.column("Name", anchor=CENTER, width=120)
added_outputs.column("default value", anchor=CENTER, width=120)
added_outputs.column("units", anchor=CENTER, width=120)

added_outputs.heading("Name", text="Name")
added_outputs.heading("default value", text="default value")
added_outputs.heading("units", text="units")

added_outputs.tag_configure("even", background="white")
added_outputs.tag_configure("odd", background="light blue")


def add_input(input_name, def_value="nan", unit="no unit specified"):
    global row_i
    if row_i % 2 == 0:
        added_inputs.insert(parent='', index='end', values=(input_name, def_value, unit), tags=("even",))
    else:
        added_inputs.insert(parent='', index='end', values=(input_name, def_value, unit), tags=("odd",))
    row_i += 1


def add_output(input_name, def_value="nan", unit="no unit specified"):
    global row_o
    if row_o % 2 == 0:
        added_outputs.insert(parent='', index='end', values=(input_name, def_value, unit), tags=("even",))
    else:
        added_outputs.insert(parent='', index='end', values=(input_name, def_value, unit), tags=("odd",))
    row_o += 1


def clear_inputs():
    added_inputs.delete(*added_inputs.get_children())
    global inputs
    global units_i
    inputs = []
    units_i = []


def clear_outputs():
    added_outputs.delete(*added_outputs.get_children())
    global outputs
    global units_o
    outputs = []
    units_o = []


fileGen_b = Button(root, text="Create file", command=generation, bg="light blue")
clearInputs_b = Button(root, text="Clear all inputs", command=clear_inputs, bg="pink")
clearOutputs_b = Button(root, text="Clear all outputs", command=clear_outputs, bg="pink")

lab1.grid(column=0, row=0, padx=10, pady=5)
lab2.grid(column=2, row=0, padx=10, pady=5)
lab3.grid(column=0, row=1, padx=10, pady=5)
lab4.grid(column=2, row=1, padx=10, pady=5)
lab5.grid(column=0, row=4, padx=10, pady=5)

e1.grid(column=1, row=0, padx=10, pady=5)
e2.grid(column=3, row=0, padx=10, pady=5)
e3.grid(column=1, row=1, padx=10, pady=5)
e4.grid(column=3, row=1, padx=10, pady=5)
text_box.grid(column=1, row=4, columnspan=4, padx=10, pady=5)
added_inputs.grid(column=0, row=2, columnspan=2, padx=10, pady=5)
added_outputs.grid(column=2, row=2, columnspan=2, padx=10, pady=5)

e1.bind("<Return>", f1)
e2.bind("<Return>", f2)
e3.bind("<Return>", f3)
e4.bind("<Return>", f4)

fileGen_b.grid(column=0, row=6, columnspan=4, ipadx=30, padx=10, pady=10)
clearInputs_b.grid(column=0, row=3, columnspan=2, padx=10, pady=5)
clearOutputs_b.grid(column=2, row=3, columnspan=2, padx=10, pady=5)

root.mainloop()
