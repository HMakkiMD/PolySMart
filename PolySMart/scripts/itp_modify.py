'''
edit input .itp file to an arranged and ordered .itp file

How to run:
    > python3 itp_modify.py 'filename'.itp
30.03.2022
'''
from itp_merge import table_format_string7
from itp_merge import table_format_string8

def itp_modify(filename):
    with open(filename) as f:
        lines = f.readlines()
        with open(filename[:-4]+'_modified.itp', 'w') as g:
            for x in range(len(lines)):
                temp = lines[x].split()
                # delete lines with comments or empty lines
                if (temp == [] or temp[0][0] == ';' or temp[0][0] == '#'):
                    temp, lines[x] = [''], ''
                # delete comments in lines
                fl = True
                counter = 0
                for i in range(len(temp)):
                    if fl == False:
                        temp[i] = ''
                        counter += 1
                    else:
                        for j in range(len(temp[i])):
                            if temp[i][j] == (';' or '#'):
                                temp[i] = temp[i][:j]
                                fl = False
                                break
                for i in range(counter):
                    temp.remove('')
                    
                try:
                    # check if the first word in line is a number or not
                    bool(int(temp[0])) == bool(int(temp[0]))
                except ValueError or IndexError:
                    if temp == ['']:
                        pass
                    else:
                        if len(temp) == 1 and temp[0][0] == '[':
                            g.write(f'[ {temp[0][1:-1]} ]\n')
                        elif len(temp)  == 3 and temp[0][0] == '[':
                            g.write(f'[ {temp[1]} ]\n')
                        else:
                            g.write(f'{lines[x]}')
                else:
                    try:
                        # check if the second word in line is a number or not
                        bool(int(temp[1])) == bool(int(temp[1]))
                    except ValueError:
                        # write atoms section in this form
                        if len(temp) == 7:
                            section_format = table_format_string7
                        elif len(temp) == 8:
                            section_format = table_format_string8
                        g.write(section_format %(*temp[:len(temp)],))
                    else:
                        # write other sections in this form
                        for y in range(len(temp)):
                            g.write('%7s  ' %(temp[y]))
                        g.write('\n')

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    itp_modify(filename)
