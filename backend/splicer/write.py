"""
Write g code (currently for testing)
"""

# load in initial_script.gcode (g code file)
with open("initial_script.gcode") as f:
    data = f.readlines()


# modify temp as specified
def set_temp(bed, hotend):
    for j in data:
        if j[:4] == 'M140':
            data[data.index(j)] = 'M140 S' + str(bed) + '\n'
        elif j[:4] == 'M190':
            data[data.index(j)] = 'M190 S' + str(bed) + '\n'
        elif j[:4] == 'M104':
            data[data.index(j)] = 'M104 S' + str(hotend) + '\n'
        elif j[:4] == 'M109':
            data[data.index(j)] = 'M109 S' + str(hotend) + '\n'
    return data


def add_end(end_only = False):
    """
    splices the end sequence onto the gcode, option to return either just the end or the entire data w/ end
    :return:
    """
    with open("end_script.gcode") as f:
        end = f.readlines()
    for li in end:
        data.append(li)
    if end_only:
        return end
    else:
        return data


def get_body_script(script_file, start_script, end_script):
    """
    cuts off start and end parts of given script and returns the actual "body"
    :return:
    """
    with open(script_file) as f:
        info = f.readlines()

    # print(info)
    # print("Start:", start_script)

    # remove starting seq
    for j in info:
        if j == start_script[-1]:
            # print(start_script[-1])
            # print(info.index(j) + 1)
            del info[:info.index(j) + 1]
            break

    # print(info)

    # remove end seq
    for j in info:
        if j == end_script[0]:
            del info[info.index(j):]
            break

    # print(info)

    return info


def construct_script(start, body, end):
    total_script = []
    total_script.extend(start)
    total_script.extend(body)
    total_script.extend(end)
    return total_script


start_seq = set_temp(60, 230).copy()
end_seq = add_end(True)
body_seq = get_body_script("test tower.gcode", start_seq, end_seq)

f = open("new.gcode", "w")
for i in construct_script(start_seq, body_seq, end_seq):
    f.write(i)
f.close()

# print(get_body_script("test tower.gcode", ))
