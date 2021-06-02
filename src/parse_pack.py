class Pack:
    def __init__(self, name='default_pack', short=False, nick='def_pack'):
        self.name = name
        self.short = short
        self.nick = nick

    def __str__(self):
        return "|" + self.name + "||" + str(self.short) + "||" + self.nick + '|'


def parse_pack(str):
    spt = str.split(',')
    pack = []
    for x in spt:
        x = x.strip()
        if 'as' in x:
            y = x.split('as')
            p = Pack(name=y[0].strip(), short=True, nick=y[1].strip())
        else:
            p = Pack(name=x)
        pack.append(p)
    return pack


def string_pack(pack):
    s = ""
    for p in pack:
        if p.short:
            s += "import {} as {}\n".format(p.name, p.nick)
        else:
            s += "import {}\n".format(p.name)
    return s


PACKS = "numpy as np, math as mat, importlib, ipyvuetify"


def main():
    print(string_pack(parse_pack(PACKS)))


if __name__ == '__main__':
    main()
