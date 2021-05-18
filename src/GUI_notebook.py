import ipywidgets as widgets
import ipyvuetify as v
import ipysheet
import global_string_gen as generate_string
from global_filegen import generate_file
from parse_values import parse_values
import numpy as np
from IPython.display import display, Markdown

RESULT = []
IN = []
D_VALUES = {}


def init(In=[]):
    global RESULT
    RESULT = []

    global IN
    IN = In

    global D_VALUES
    D_VALUES = {}

    global copy_but
    copy_but = v.Btn(children=['Copy cells'], color='blue lighten-1', height='55px', width='250px')
    copy_but.on_event('click', copy_click)

    global copy_field_1
    copy_field_1 = v.TextField(v_model="1", color='blue lighten-4', outlined=True, label='First cell')

    global copy_field_2
    copy_field_2 = v.TextField(v_model="2", color='blue lighten-4', outlined=True, label='Last cell')

    global analyse_but
    analyse_but = v.Btn(children=['Analyse'], color='blue lighten-1')
    analyse_but.on_event('click', analyse_click)

    global print_but
    print_but = v.Btn(children=['Print code'], color='orange lighten-2')
    print_but.on_event('click', print_click)

    global gen_but
    gen_but = v.Btn(children=['Generate file'], color="green lighten-2")
    gen_but.on_event('click', gen_click)

    global numpy_check
    numpy_check = v.Checkbox(label="import numpy", v_model=True)

    global function
    function = v.Textarea(
        v_model='# Component1\ny = x + 1',
        label='Equations',
        clearable=True,
        rounded=True,
        auto_grow=False,
        rows=15,
        background_color="blue lighten-4"
    )

    global hb
    hb = widgets.Box(children=[copy_but, copy_field_1, copy_field_2])
    hb.layout.display = 'flex'
    hb.layout.border = '2px'
    hb.layout.justify_content = 'space-around'
    hb.layout.width = '75%'

    global vb
    vb = widgets.VBox(children=[hb, function, analyse_but])
    return vb


def copy_click(widget, event, data):
    n1 = int(copy_field_1.v_model)
    n2 = int(copy_field_2.v_model) + 1
    copy = ""
    global D_VALUES
    if 0 < n1 < n2 <= len(IN):
        for cell in IN[n1:n2]:
            if len(cell) >= 9:
                if cell[0:9] != '# Exclude':
                    copy += cell + "\n"
                else:
                    parse_values(cell, D_VALUES)
            else:
                copy += cell + "\n"
    function.v_model = copy


def analyse_click(widget, event, data):
    analyse_but.loading = True
    analyse_but.disabled = True

    in_str = function.v_model
    result = generate_string.total_parse(in_str)
    n = 0
    for g in result:
        for c in g[1]:
            n += len(c.var_in)
            n += len(c.var_out)

    headers = ['Group Name', 'Component Name', 'Variable Detected', 'Variable Name', 'Input/Output', 'Units',
               'Default Value']

    sheet = ipysheet.sheet(columns=7, rows=n, row_headers=False, column_headers=headers)

    i = 0
    for g in result:
        for c in g[1]:
            for var_in in c.var_in:
                ipysheet.cell(i, 0, c.group, background_color='#EEEEEE', read_only=True)
                ipysheet.cell(i, 1, c.name, background_color='#EEEEEE', read_only=True)
                ipysheet.cell(i, 2, var_in[0])
                ipysheet.cell(i, 3, var_in[1])
                ipysheet.cell(i, 4, 'input', background_color='#8EFF9B', read_only=True)
                ipysheet.cell(i, 5, 'None')
                ipysheet.cell(i, 6, 'np.nan')
                if var_in[0] in D_VALUES:
                    ipysheet.cell(i, 6, D_VALUES[var_in[0]])
                i += 1
            for j in range(len(c.var_out)):
                var_out = c.var_out[j]
                ipysheet.cell(i, 0, c.group, background_color='#EEEEEE', read_only=True)
                ipysheet.cell(i, 1, c.name, background_color='#EEEEEE', read_only=True)
                ipysheet.cell(i, 2, var_out[0])
                ipysheet.cell(i, 3, var_out[1])
                ipysheet.cell(i, 4, 'output', background_color='#FFB48E', read_only=True)
                ipysheet.cell(i, 5, c.units_o[j])
                ipysheet.cell(i, 6, '', background_color='#EEEEEE', read_only=True)
                i += 1

    analyse_but.loading = False
    analyse_but.children = ['Analysis done']
    function.background_color = "#C0C0C0"
    vb.children = (list(vb.children) + [sheet, numpy_check, print_but, gen_but])

    global RESULT
    RESULT = result


def print_click(widget, event, data):
    # Function called when the button 'print code' is pressed

    print_but.loading = True
    print_but.disabled = True

    sheet = ipysheet.current()
    arr = np.array([])
    arr = ipysheet.to_array(sheet)

    global RESULT

    result = RESULT

    i = 0
    for g in result:
        for c in g[1]:
            j = 0
            jl = []
            for var_in in c.var_in:
                var_in[0] = arr[i, 2]
                var_in[1] = arr[i, 3]
                c.units_i[j][0] = arr[i, 5]
                c.units_i[j][1] = arr[i, 6]
                if var_in[1] == "del":
                    c.var_in.remove(var_in)
                    jl.append(j)
                i += 1
                j += 1
            for n in jl:
                c.units_i.pop(n)
            k = 0
            kl = []
            for var_out in c.var_out:
                var_out[0] = arr[i, 2]
                var_out[1] = arr[i, 3]
                c.units_o[k] = arr[i, 5]
                if var_out[1] == "del":
                    c.var_out.remove(var_out)
                    kl.append(k)
                i += 1
                k += 1
            for n in kl:
                c.units_o.pop(n)

    print_but.loading = False
    print_but.children = ['Code printed']

    s = generate_string.gen_string(result, numpy_check.v_model)
    display(Markdown("```python\n" + s + "\n```"))


def gen_click(widget, event, data):
    # Function called when the button 'generate file' is pressed

    gen_but.loading = True
    gen_but.disabled = True

    sheet = ipysheet.current()
    arr = np.array([])
    arr = ipysheet.to_array(sheet)

    global RESULT

    result = RESULT
    # Modifying result to take into account changes made to the sheet
    i = 0
    for g in result:
        for c in g[1]:
            j = 0
            jl = []
            for var_in in c.var_in:
                var_in[0] = arr[i, 2]
                var_in[1] = arr[i, 3]
                c.units_i[j][0] = arr[i, 5]
                c.units_i[j][1] = arr[i, 6]
                if var_in[1] == "del":
                    c.var_in.remove(var_in)
                    jl.append(j)
                i += 1
                j += 1
            for n in jl:
                c.units_i.pop(n)
            k = 0
            kl = []
            for var_out in c.var_out:
                var_out[0] = arr[i, 2]
                var_out[1] = arr[i, 3]
                c.units_o[k] = arr[i, 5]
                if var_out[1] == "del":
                    c.var_out.remove(var_out)
                    kl.append(k)
                i += 1
                k += 1
            for n in kl:
                c.units_o.pop(n)

    gen_but.loading = False
    gen_but.children = ['File generated ']

    generate_file(result, numpy_check.v_model)


def init_click(widget, event, data):
    init()


copy_but = v.Btn()

copy_field_1 = v.TextField()

copy_field_2 = v.TextField()

analyse_but = v.Btn()

print_but = v.Btn()

gen_but = v.Btn()

numpy_check = v.Checkbox()

function = v.Textarea()

hb = widgets.Box()

vb = widgets.VBox()
