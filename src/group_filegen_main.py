from group_filegen import gen_group_file


def main():
    print("om.Group file generator")
    f_name = input("File name(no extension):")
    g_name = input("Group name:")
    subsystems = []
    init = 0

    yn = input("Do you want an initialize function ?(Y/N)")
    if yn == 'Y':
        init = input("Content of the initialize function:")
    yn = 'Y'

    while yn == 'Y':
        s_name = input("Subsystem_name:")
        c_name = input("Class name:")
        p_name = input("Package name:")
        subsystems.append([s_name, c_name, p_name])
        yn = input("New subsystem ?(Y/N)")

    gen_group_file(f_name, g_name, subsystems, init)
    print("---file generated---\n")


if __name__ == '__main__':
    main()
