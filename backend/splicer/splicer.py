"""
Based on given settings, create a spliced g code series with certain features
"""


# INPUT = "CE3_Reservoir A.gcode"
# OUTPUT = "Reservoir_Sequential.gcode"
# INPUT = "Sunlu Res A.gcode"
# OUTPUT = "2x RES A.gcode"


def add_simultaneous_heating(code_list):
    """
    Moves heating commands to heat build plate and hot end simultaneously (efficiency)
    :param code_list: a list of lines of g code
    :return: the modified list of g code
    """
    for ln in code_list:
        # each line is a string
        if ln[:4] == 'M190':
            cut = ln
            code_list.remove(ln)
        if ln[:6] == 'M109 S' and cut is not None:
            # print(ln)
            code_list.insert(code_list.index(ln), cut)
            break
    return code_list


def add_print_removal(code_list):
    """
    Adds a print bumping function at the end of the g code
    :param code_list: a list of lines of g code
    :return: the modified list of g code
    """
    add_list = []  # gcode to be added

    # cooldown time
    add_list.append("; Allowing bed to cool down\n")

    release_temp = 33

    add_list.append(
                    "M140 R" + str(release_temp) + "; Set temp to " + str(release_temp) + "deg\n"
                    "M105; Display temp to LCD\n"
                    "M190 R" + str(release_temp) + "; Wait for temp to go down\n"
                    )

    # add more commands to override timeout
    for i in range(8):
        add_list.append("M190 R" + str(release_temp) + "; Wait for temp to go down some more\n")

    add_list.append("; Print removal starting!\n")

    add_list.append("G1 X0 Y235 F10000.0; move to back left corner\n")
    add_list.append("G1 Z0 F10000.0; move down to scrape height\n")

    x = -50
    while x < 100:  # 235
        x += 50
        if x > 235:
            x = 235
        add_list.append("G1 X" + str(x) + " Y235 F10000.0\n")  # starting move (x only)
        add_list.append("G1 X" + str(x) + " Y0 F10000.0\n")  # swipe down
        add_list.append("G1 X" + str(x) + " Y235 F10000.0\n")  # come back

    print(add_list)

    # replace the end, where the g code presents the print, with going behind the print and knocking it off
    for ln in code_list:
        if ln[:7] == 'G1 X0 Y':
            print(ln)
            print(code_list.index(ln))
            # code_list = code_list[:code_list.index(ln) + 1] + add_list + code_list[code_list.index(ln) + 1:]
            code_list = code_list[:code_list.index(ln)] + add_list + code_list[code_list.index(ln) + 1:]
            for i in code_list:
                if i == 'G1 X0 Y235 ;Present print\n':
                    print("YES")
            # print("CODE LIST:", code_list)

    # print(code_list)
    return code_list


def add_cooldown(code_list, bed_target, hotend_target):
    # load in bed_cool_sequence.gcode (g code file)
    with open("Insertion files/bed_cool_sequence.gcode") as f:
        cooldown = f.readlines()
    for ln in cooldown:
        find_string = 'M140 S'
        if ln[:len(find_string)] == find_string:
            print("yes")
            cooldown[cooldown.index(ln)] = 'M140 R' + str(bed_target) + "\n"
    for ln in cooldown:
        find_string = 'M104 S'
        if ln[:len(find_string)] == find_string:
            print("yes1")
            cooldown[cooldown.index(ln)] = 'M104 S' + str(hotend_target) + "\n"
    for ln in cooldown:
        find_string = 'M190 S'
        if ln[:len(find_string)] == find_string:
            print("yes2")
            cooldown[cooldown.index(ln)] = 'M190 R' + str(bed_target) + "\n"
    for ln in cooldown:
        find_string = 'M109 S'
        if ln[:len(find_string)] == find_string:
            print("yes3")
            cooldown[cooldown.index(ln)] = 'M109 S' + str(hotend_target) + "\n"
    for ln in code_list:
        # each line is a string
        find_string = 'G1 X0 Y235 ;Present print'
        if ln[:len(find_string)] == find_string:
            print("yes4")
            code_list = code_list[:code_list.index(ln) + 1] + cooldown + code_list[
                                                                         code_list.index(ln) + 1:]  # insert cool
            break
    return code_list


def duplicate(code_list, no_instances):
    initial_list = code_list.copy()
    for j in range(no_instances):
        code_list = code_list + initial_list
    return code_list


def splice(INPUT, OUTPUT, no_duplicates):
    # load in initial_script.gcode (g code file)
    print("Opening:", INPUT, "...")
    with open(INPUT) as f:
        data = f.readlines()

    script = data.copy()  # get initial gcode
    print("Splicing", no_duplicates, "instances...")
    add_simultaneous_heating(script)
    script = add_print_removal(script)
    script = duplicate(script, no_duplicates-1)

    print("Writing to:", OUTPUT, "...")
    f = open(OUTPUT, "w")
    for i in script:
        # print(i)
        f.write(i)
    f.close()

