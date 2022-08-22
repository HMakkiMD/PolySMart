'''
Merge input .itp files to one .itp file

How to run:
    > python3 itp_merge.py 'number of molecule types' 'molecule1'.itp 'number' 'molecule2'.itp 'number' ,... 'output'.itp
11.03.2022
'''

table_format_string7 = '%7s\t %-7s%6s   %-5s  %-6s  %7s   %-5s\n'
table_format_string8 = '%7s\t %-7s%6s   %-5s  %-6s  %7s   %-5s   %-7s\n'

headerlist = [
    '[ atoms ]',
    '[ bonds ]',
    '[ angles ]',
    '[ dihedrals ]',
    '[ constraints ]',
    '[ virtual_sitesn ]',
    '[ exclusions ]',
    '[]'
]

header_to_count = {
    "[ bonds ]" : 2,
    "[ angles ]" : 3,
    "[ dihedrals ]" : 4,
    "[ constraints ]" : 2,
    "[ virtual_sitesn ]" : 6,
    "[ exclusions ]" : -1
}

# add is the whole number of atoms in previous molecule types and should be added to each atom number to get its new number
# addr is the whole number of residues in previous molecule types and should be added to each residue number to get its new number
# block is a list containing required lines of input file which is attributed to the desired section
# z is the counter for number of each molecule types
# y is the counter for no. of lines in each section
# at_no is the number of atoms for each molecule
def write_atoms(block, y, z, at_no, add, addr, g):
    sp = block[y].split()   # sp is a list containing splitted form of each line
    sp.insert(0, int(sp[0]) + (z * at_no) + add) # edit atom number
    sp.pop(1)
    sp.insert(2, z + 1 + addr)   # edit residue number
    sp.pop(3)
    sp.insert(5, sp[0])
    sp.pop(6)
    if add == 0 and z == 0 and y == 0:    # only for first time write the header
        g.write('[ atoms ]\n')
    if len(sp) == 7:
        section_format = table_format_string7
    elif len(sp) == 8:
        section_format = table_format_string8
    g.write(section_format %(*sp[:(len(sp))],))

def write_section(name, block, y, z, at_no, add, flag, g):
    sp = block[y].split()
    count = header_to_count[name]
    if count == -1:
        count = len(sp)

    for i in range(count):  # edit atom numbers for 2 first numbers in line
        if name != '[ virtual_sitesn ]' or i != 1:
            sp.insert(i, int(sp[i]) + (z * at_no) + add)
            sp.pop(i+1)
    if (add == 0 and z == 0 and y == 0) or flag is False:
        g.write(f'{name}\n')
    for j in range(len(sp)):
        g.write('%7s  ' %(sp[j]))
    g.write('\n')

def itp_merge(type_no, file_paths, numbers, out_path):
    # Writing [moleculetype] section in itp file
    with open(out_path, 'w') as f:
        f.write('[ moleculetype ]\nMixture 1\n')

    # Finding the position of [atoms], [bonds] and etc. in input itp files
    # m is the counter for molecule types
    files = []
    atom_nos = []
    headerlists = []
    for m in range(type_no):
        if file_paths[m][-4:] != '.itp':
            file_paths[m] += '.itp'
        with open (file_paths[m]) as f:
            i = -1
            headers = {}
            files.append(f.readlines())
            for line in files[m]:
                i += 1
                for header in headerlist:
                    if header in line and header != '[]':
                        headers[i] = header

            sorted_keys = sorted(headers.keys()) # sort the dict by keys
            sorted_headers = {}
            for j in sorted_keys:
                for k in headers.values():
                    if headers[j] == k:
                        sorted_headers[j] = headers[j]
                        break
            headers = sorted_headers
            items = list(headers.items()) # conert the dict to list
            items.append((i + 1, '')) # add the end line
            headerlists.append(items)
            atom_nos.append(headerlists[m][1][0] - headerlists[m][0][0] - 1) # find no. of atoms from no. of lines in [atoms] section

    # adding new lines in each section of itp files
    with open(out_path, 'a') as g:
        for x in range(len(headerlist)-1):  # x is the counter for each section
            m = 0                           # m is the counter for molecule types
            add = 0
            addr = 0
            flag = False # assessing that the last molecule had this section or not
            for m in range(type_no):
                at_no = atom_nos[m]
                t = 0
                for t in range(len(headerlists[m])): # finding the desired section in molecule
                    if headerlists[m][t][1] == headerlist[x]:
                        header = headerlists[m][t][1]
                        header_value = headerlists[m][t][0]
                        next_header_value = headerlists[m][t + 1][0]
                        block = files[m][header_value + 1 : next_header_value + 1]
                        for z in range(numbers[m]): # z is the counter for number of each molecule types
                            # y is the counter for no. of lines in each section
                            for y in range(next_header_value - header_value - 1):
                                # if the section is attributed to atoms add new lines in this format:
                                if header == '[ atoms ]':
                                    write_atoms(block, y, z, at_no, add, addr, g)
                                elif next_header_value - header_value > 1:
                                    for i_header in header_to_count.keys():
                                        if header == i_header:
                                            write_section(header, block, y, z, at_no, add, flag, g)
                                flag = True
                add += numbers[m] * at_no
                addr += numbers[m] * (m + 1)
        g.write(' ')
    # check that there is solvent in system or not to make .top file
    try:
        with open('../data/inputs.txt') as g:
            pass
    except FileNotFoundError:
        flag2 = False
    else:
        flag2 = True
        with open('../data/inputs.txt') as g:
            inp_line = g.readline().split()
        try:
            inp_line[5], inp_line[6]
        except IndexError:
            flag2 = False
        else:
            flag2 = True
    with open('../topol.top', 'w') as g:
        g.write('#include "data/martini_v3.0.0.itp"\n\n')
        if flag2 is True:
            for c in range(5, len(inp_line), 2):
                g.write(f'#include "data/{inp_line[c]}.itp"\n')
        if out_path[:3] == '../':
            out_name = out_path[3:]
        else:
            out_name = out_path
        g.write(f'#include "{out_name}"\n\n')
        g.write('[ system ]\n')
        g.write('Mixture\n\n')
        g.write('[ molecules ]\n')
        g.write('Mixture    1\n')
        if flag2 is True:
            for c in range(5, len(inp_line), 2):
                g.write(f'{inp_line[c]}    {inp_line[c+1]}\n')

if __name__ == '__main__':
    import sys
    # Reading molecule types, file names and numbers from input
    file_paths, numbers = [], []
    type_no = int(sys.argv[1])
    for n in range(type_no):
        file_paths.append(sys.argv[2 * n + 2])
        numbers.append(int(sys.argv[2 * n + 3]))
    out_path = sys.argv[2 * n + 4]
    itp_merge(type_no, file_paths, numbers, out_path)
