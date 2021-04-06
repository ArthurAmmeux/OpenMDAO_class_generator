from group_print import print_group


def main():
    print("om.Group print")
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

    print("---code---\n")
    print_group(g_name, subsystems, init)


if __name__ == '__main__':
    main()
