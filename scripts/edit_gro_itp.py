"""
Edit .gro and .itp file after each loop of reaction.

How to run:
    > python3 edit_gro_itp.py 'XL'.txt 'filename'.gro 'filename'.itp 'loop_x'.txt
"""
def edit_gro_itp(XL, gro_filename, itp_filename, loop_x):
    from itp_merge import table_format_string7
    from itp_merge import table_format_string8
    from random import random
    
    # read lines of input.txt and assign parameters
    with open('../data/inputs.txt') as f:
        lis = f.readlines()
        for i in range(4, len(lis)):
            lis[i] = lis[i].split()        
    with open(XL) as f:
        xlfilelist = f.readlines() # read the reacting pairs file
    length = len(xlfilelist)
    
    br = []
    
    try:
        with open('../data/break.txt') as f:
            pass
    except FileNotFoundError:
        pass
    else:
        with open('../data/break.txt') as f:
            br = f.readlines()
            for i in range(len(br)):
                br[i] = br[i].split()
    
    with open(itp_filename , 'r') as f:
        i, bond_line, angle_line, dihedral_line, constraint_line, virtual_line, \
            exclusion_line = 0,0,0,0,0,0,0
        filelist = f.readlines()
        # find the starting position of each section
        for line in filelist:
            if '[ bonds ]' in line:
                bond_line = i
            if '[ angles ]' in line:
                angle_line = i
            if '[ dihedrals ]' in line and dihedral_line == 0:
                dihedral_line = i
            if '[ constraints ]' in line:
                constraint_line = i
            if '[ virtual_sitesn ]' in line:
                virtual_line = i
            if '[ exclusions ]' in line:
                exclusion_line = i
            i += 1
        end_line = i - 1
        
        # make a new list consisting all bonds and constraints
        if bond_line != 0:  # find the end line of bonds
            if angle_line == 0:
                if dihedral_line == 0:
                    if constraint_line == 0:
                        if virtual_line == 0:
                            if exclusion_line == 0:
                                bond_end = i - 1
                            else:
                                bond_end = exclusion_line
                        else:
                            bond_end = virtual_line
                    else:
                        bond_end = constraint_line
                else:
                    bond_end = dihedral_line
            else:
                bond_end = angle_line
            bonds_list = filelist[bond_line+1:bond_end]
        else:
            bonds_list = []
        if constraint_line != 0: # find the end line of constraints
            if virtual_line == 0:
                if exclusion_line == 0:
                    constraint_end = i - 1
                else:
                    constraint_end = exclusion_line
            else:
                constraint_end = virtual_line
            constraint_list = filelist[constraint_line+1:constraint_end]
            bonds_list.extend(constraint_list)
        bonds_set = []
        for i in range(len(bonds_list)):
            bonds_set.append({bonds_list[i].split()[0], bonds_list[i].split()[1]})     
    
    delete = set() # used set instead of list to not keep duplicates
    items = []
    itemslist = []

    # check for beads which are near to two reacting beads and keep only the first one
    for i in range(length):
        line1 = xlfilelist[i].split()
        if {line1[1], line1[3]} in bonds_set:
            delete.add(i)
        else:
            for j in range(i+1,length):
                line2 = xlfilelist[j].split()
                if line1[1] == line2[1] or line1[3] == line2[3] or line1[1] == line2[3] or line1[3] == line2[1]:
                    delete.add(j) # set of repetitious beads which should be deleted
    delete = list(delete)
    delete.sort()
    delete.reverse()
    for n in range(len(delete)):
        xlfilelist.pop(delete[n]) # delete repetitious beads from reacting pairs list
    for m in range(len(xlfilelist)):
        items.append((xlfilelist[m].split()[1],xlfilelist[m].split()[3],\
                    xlfilelist[m].split()[0],xlfilelist[m].split()[2])) # add reacting pairs to a list
        itemslist.append(xlfilelist[m].split()[1]) # add reacting beads to a list
        itemslist.append(xlfilelist[m].split()[3]) # add reacting beads to a list
    # write a file containing modified reacting pairs
    with open(loop_x , 'w') as f:
        f.writelines(xlfilelist)

    # edit .gro file
    with open(gro_filename , 'r+') as f:
        f.readline() # pass the first two lines of .gro file
        f.readline()
        counter = f.tell() # starting point for bead lines
        for k in range(len(itemslist)):
            f.seek(counter+10+45*(int(itemslist[k])-1)) # position of the bead name
            sp = f.readline().split()
            f.seek(counter+10+45*(int(itemslist[k])-1))
            # check if the bead had been reacted in previous steps (for beads that can react more than one time)
            if (sp[0][0] != '1') and (sp[0][0] != '2') and (sp[0][0] != '3'):
                new_bead_name = '1'+sp[0]
                if (int(itemslist[k]) > 9999) and (int(itemslist[k]) < 100000):
                    new_bead_name = new_bead_name[:-5]
                f.write('%5s' %(new_bead_name))
            elif sp[0][0] == '1':
                new_bead_name = '2'+sp[0][1:]
                if (int(itemslist[k]) > 9999) and (int(itemslist[k]) < 100000):
                    new_bead_name = new_bead_name[:-5]
                f.write('%5s' %(new_bead_name))
            elif sp[0][0] == '2':
                new_bead_name = '3'+sp[0][1:]
                if (int(itemslist[k]) > 9999) and (int(itemslist[k]) < 100000):
                    new_bead_name = new_bead_name[:-5]
                f.write('%5s' %(new_bead_name))
            elif sp[0][0] == '3':
                new_bead_name = '4'+sp[0][1:]
                if (int(itemslist[k]) > 9999) and (int(itemslist[k]) < 100000):
                    new_bead_name = new_bead_name[:-5]
                f.write('%5s' %(new_bead_name))

    # edit .itp file
    # edit [atoms] section of itp file
    for l in range(len(items)):
        for x in range(4, len(lis)): # find the bead types of the pair beads after reaction
            if (lis[x][0] == items[l][2]) and (lis[x][1] == items[l][3]):
                beadname1 = lis[x][5]
                beadname2 = lis[x][6]
                break
            elif (lis[x][0] == items[l][3]) and (lis[x][1] == items[l][2]):
                beadname1 = lis[x][6]
                beadname2 = lis[x][5]
                break
        line = filelist[int(items[l][0])+2].split()
        if len(line) == 7:
            section_format = table_format_string7
        elif len(line) == 8:
            section_format = table_format_string8
        if (line[4][0] != '1') and (line[4][0] != '2') and (line[4][0] != '3'): # if the bead is reacting for first time
            filelist.insert(int(items[l][0])+2, section_format %(line[0],beadname1,line[2],line[3],'1'+line[4],*line[5:len(line)],))
        elif line[4][0] == '1': # if the bead is reacting for second time(for beads that can react more than one time)
            filelist.insert(int(items[l][0])+2, section_format %(line[0],beadname1,line[2],line[3],'2'+line[4][1:],*line[5:len(line)],))
        elif line[4][0] == '2': # if the bead is reacting for third time(for beads that can react more than one time)
            filelist.insert(int(items[l][0])+2, section_format %(line[0],beadname1,line[2],line[3],'3'+line[4][1:],*line[5:len(line)],))
        elif line[4][0] == '3': # if the bead is reacting for second time(for beads that can react more than one time)
            filelist.insert(int(items[l][0])+2, section_format %(line[0],beadname1,line[2],line[3],'4'+line[4][1:],*line[5:len(line)],))
        filelist.pop(int(items[l][0])+3)
        line = filelist[int(items[l][1])+2].split()
        if len(line) == 7:
            section_format = table_format_string7
        elif len(line) == 8:
            section_format = table_format_string8
        if (line[4][0] != '1') and (line[4][0] != '2') and (line[4][0] != '3'): # if the bead is reacting for first time
            filelist.insert(int(items[l][1])+2, section_format %(line[0],beadname2,line[2],line[3],'1'+line[4],*line[5:len(line)],))
        elif line[4][0] == '1': # if the bead is reacting for second time(for beads that can react more than one time)
            filelist.insert(int(items[l][1])+2, section_format %(line[0],beadname2,line[2],line[3],'2'+line[4][1:],*line[5:len(line)],))
        elif line[4][0] == '2': # if the bead is reacting for third time(for beads that can react more than one time)
            filelist.insert(int(items[l][1])+2, section_format %(line[0],beadname2,line[2],line[3],'3'+line[4][1:],*line[5:len(line)],))
        elif line[4][0] == '3': # if the bead is reacting for second time(for beads that can react more than one time)
            filelist.insert(int(items[l][1])+2, section_format %(line[0],beadname2,line[2],line[3],'4'+line[4][1:],*line[5:len(line)],))
        filelist.pop(int(items[l][1])+3)
        
    # search in bonds list for each reacting bead and find out that the bead is connected to which other beads (to determine new angles)
    bonds_found = []
    marked_beads = [] # beads that are connected to beads that are connected to reacting beads (to determine new dihedrals)
    bonds_found2 = [] # all bonds that have any of marked_beads
    for q in range(len(bonds_list)):
        sp = bonds_list[q].split()
        for l in range(len(items)):
            for x in range(2):
                if items[l][x] == sp[0]:
                    bonds_found.append((sp[1],sp[0]))
                    marked_beads.append(sp[1])
                elif items[l][x] == sp[1]:
                    bonds_found.append((sp[0],sp[1]))
                    marked_beads.append(sp[0])
#    marked_beads = list(set(marked_beads)-set(itemslist).intersection(set(marked_beads)))
    for q in range(len(bonds_list)):
        sp = bonds_list[q].split()
        for l in range(len(marked_beads)):
            if ((marked_beads[l] == sp[0]) and (sp[1] not in itemslist)) or \
                ((marked_beads[l] == sp[1]) and (sp[0] not in itemslist)):
                bonds_found2.append((sp[0],sp[1]))

    # determine the insertion point for new bonds
    if angle_line != 0:
        insert_point = angle_line
    elif dihedral_line != 0:
        insert_point = dihedral_line
    elif constraint_line != 0:
        insert_point = constraint_line
    elif virtual_line != 0:
        insert_point = virtual_line
    elif exclusion_line != 0:
        insert_point = exclusion_line
    else:
        insert_point = end_line

    flag = True
    if bond_line == 0: # if there was no bonds in file then header [bonds] should be added
        filelist.insert(insert_point, '[ bonds ]\n')
        insert_point += 1
        flag = False
    
    # edit bonds that are connected to reacting beads in [bonds] section
    try:
        with open('../data/existing_bonds.txt') as g:
            g.readlines()
    except FileNotFoundError or NameError:
        pass
    else:
        with open('../data/existing_bonds.txt') as g:
            ex_bonds = g.readlines()
        for x in range(len(ex_bonds)):
            ex_bonds[x] = ex_bonds[x].split()
            if (bond_line != 0 and ex_bonds[x] != []):
                for y in range(bond_line+1,bond_end):
                    # check if the bond is connected to the new bond
                    if sorted(filelist[y].split()[:2]) in list(sorted(bonds_found[z]) for \
                                                       z in range(len(bonds_found))):
                        # check if the bond should be modified
                        if (ex_bonds[x][0] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_bonds[x][1] == filelist[int(filelist[y].split()[1])+2].split()[1]) or \
                           (ex_bonds[x][1] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_bonds[x][0] == filelist[int(filelist[y].split()[1])+2].split()[1]):
                            filelist.insert(y, '%7s  %7s  %7s  %7s  %7s\n' \
                                    %(filelist[y].split()[0],filelist[y].split()[1],'1',\
                                              ex_bonds[x][2],ex_bonds[x][3]))
                            filelist.pop(y + 1)
            # do the same for constraints
            if (constraint_line != 0 and ex_bonds[x] != []):
                for y in range(constraint_line+1,constraint_end):
                    if sorted(filelist[y].split()[:2]) in list(sorted(bonds_found[z]) for \
                                                       z in range(len(bonds_found))):
                        if (ex_bonds[x][0] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_bonds[x][1] == filelist[int(filelist[y].split()[1])+2].split()[1]) or \
                           (ex_bonds[x][1] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_bonds[x][0] == filelist[int(filelist[y].split()[1])+2].split()[1]):
                            filelist.insert(y, '%7s  %7s  %7s  %7s  %7s\n' \
                                    %(filelist[y].split()[0],filelist[y].split()[1],'1',\
                                              ex_bonds[x][2],ex_bonds[x][3]))
                            filelist.pop(y + 1)
    
    # adding new bonds to file list
    bond_nos = 0
    for x in range(len(items)):
        for y in range(4, len(lis)): # find the bead types of the pair beads after reaction
            if (lis[y][0] == items[x][2]) and (lis[y][1] == items[x][3]) or \
                (lis[y][0] == items[x][3]) and (lis[y][1] == items[x][2]):
                bond_dist = lis[y][7]
                bond_const = lis[y][8]
                filelist.insert(insert_point+bond_nos, '%7s  %7s  %7s  %7s  %7s\n' \
                        %(items[x][0], items[x][1], '1', bond_dist, bond_const))
                bond_nos += 1
                break

    # determine the insertion point for new angles
    if dihedral_line != 0:
        insert_point = dihedral_line
    elif constraint_line != 0:
        insert_point = constraint_line
    elif virtual_line != 0:
        insert_point = virtual_line
    elif exclusion_line != 0:
        insert_point = exclusion_line
    else:
        insert_point = end_line
    flag2 = True
    if angle_line == 0: # if there was no angles in file then header [angles] should be added
        if flag is False:
            filelist.insert(insert_point+bond_nos+1, '[ angles ]\n')
            insert_point += 1
        elif flag is True:
            filelist.insert(insert_point+bond_nos, '[ angles ]\n')
        insert_point += 1
        flag2 = False
    
    # edit angles that exist and their parameters should be changed due to reactions
    try:
        with open('../data/existing_angles.txt') as g:
            g.readlines()
    except FileNotFoundError or NameError:
        pass
    else:
        with open('../data/existing_angles.txt') as g:
            ex_angs = g.readlines()
        for x in range(len(ex_angs)):
            ex_angs[x] = ex_angs[x].split()
            if (angle_line != 0 and ex_angs[x] != []):
                for y in range(angle_line+bond_nos+1,insert_point):
                    # check if the angle is affected by the reaction
                    if list(value for value in filelist[y].split()[:3] if value in \
                            itemslist) != []:
                        # check if the angle should be modified
                        if (ex_angs[x][0] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_angs[x][1] == filelist[int(filelist[y].split()[1])+2].split()[1] and \
                            ex_angs[x][2] == filelist[int(filelist[y].split()[2])+2].split()[1]) or \
                           (ex_angs[x][2] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_angs[x][1] == filelist[int(filelist[y].split()[1])+2].split()[1] and \
                            ex_angs[x][0] == filelist[int(filelist[y].split()[2])+2].split()[1]):
                            filelist.insert(y, '%7s  %7s  %7s  %7s  %7s  %7s\n' \
                                    %(filelist[y].split()[0],filelist[y].split()[1],\
                                    filelist[y].split()[2],ex_angs[x][3],ex_angs[x][4],\
                                        ex_angs[x][5]))
                            filelist.pop(y + 1)

    counter = 0
    # adding new angles to file list
    with open('../data/new_angles_parameters.txt') as f:
        angle_types = f.readlines()
    for l in range(len(bonds_found)):
        for x in range(len(items)):
            if bonds_found[l][1] == items[x][0]:
                temp = items[x][1]
            elif bonds_found[l][1] == items[x][1]:
                temp = items[x][0]
        one = filelist[int(bonds_found[l][0]) + 2].split()[1]
        two = filelist[int(bonds_found[l][1]) + 2].split()[1]
        three = filelist[int(temp) + 2].split()[1]
        ang_type, ang_eq, ang_const = 2,0,0
        for c in range(len(angle_types)):
            ang = angle_types[c].split()
            if ang ==[]:
                pass
            elif len(ang) != 6:
                print('Wrong input angles')
                break
            elif ((two == ang[1]) and (one == ang[0]) and (three == ang[2])) or \
                ((two == ang[1]) and (one == ang[2]) and (three == ang[0])):
                ang_type = ang[3]
                ang_eq = ang[4]
                ang_const = ang[5]
        if ((ang_eq and ang_const) != 0) and (len({bonds_found[l][0], bonds_found[l][1], temp}) == 3):
            filelist.insert(insert_point+counter+bond_nos, '%7s  %7s  %7s  %7s  %7s  %7s\n' \
                    %(bonds_found[l][0], bonds_found[l][1], temp, ang_type, ang_eq, ang_const))
            counter += 1
        else:
            try:   # write undefined angles into a new file for user 
                with open('../undefined_angles.txt') as g:
                    g.readline()
            except FileNotFoundError or NameError:
                with open('../undefined_angles.txt', 'w') as g:
                    if len({bonds_found[l][0], bonds_found[l][1], temp}) == 3:
                        g.write('%7s (%7s) %7s (%7s) %7s (%7s) \n' %(bonds_found[l][0], \
                        one, bonds_found[l][1], two, temp, three))
            else:
                with open('../undefined_angles.txt', 'a') as g:
                    if len({bonds_found[l][0], bonds_found[l][1], temp}) == 3:
                        g.write('%7s (%7s) %7s (%7s) %7s (%7s) \n' %(bonds_found[l][0], \
                        one, bonds_found[l][1], two, temp, three))
                        
    # determine the insertion point for new dihedrals
    if constraint_line != 0:
        insert_point = constraint_line
    elif virtual_line != 0:
        insert_point = virtual_line
    elif exclusion_line != 0:
        insert_point = exclusion_line
    else:
        insert_point = end_line        
    if dihedral_line == 0: # if there was no dihedrals in file then header [dihedrals] should be added
        if flag is False:
            if flag2 is False:
                filelist.insert(insert_point+bond_nos+counter+2, '[ dihedrals ]\n')
                insert_point += 1
            elif flag2 is True:
                filelist.insert(insert_point+bond_nos+counter+1, '[ dihedrals ]\n')
                insert_point += 1
        elif flag is True:
            if flag2 is False:
                filelist.insert(insert_point+bond_nos+counter+1, '[ dihedrals ]\n')
                insert_point += 1
            elif flag2 is True:
                filelist.insert(insert_point+bond_nos+counter, '[ dihedrals ]\n')
        insert_point += 1
    
    # edit dihedrals that exist and their parameters should be changed due to reactions
    try:
        with open('../data/existing_dihedrals.txt') as g:
            g.readlines()
    except FileNotFoundError or NameError:
        pass
    else:
        with open('../data/existing_dihedrals.txt') as g:
            ex_dihs = g.readlines()
        for x in range(len(ex_dihs)):
            ex_dihs[x] = ex_dihs[x].split()
            if (dihedral_line != 0 and ex_dihs[x] != []):
                for y in range(dihedral_line+bond_nos+counter+1,insert_point):
                    if 'dihedrals' in filelist[y].split():
                        y += 1   # prevent error in case the line is '[ dihedrals ]
                    # check if the dihedral is affected by the reaction
                    if list(value for value in filelist[y].split()[:4] if value in \
                            itemslist) != []:
                        # check if the dihedral should be modified
                        if (ex_dihs[x][0] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_dihs[x][1] == filelist[int(filelist[y].split()[1])+2].split()[1] and \
                            ex_dihs[x][2] == filelist[int(filelist[y].split()[2])+2].split()[1] and \
                            ex_dihs[x][3] == filelist[int(filelist[y].split()[3])+2].split()[1]) or \
                           (ex_dihs[x][3] == filelist[int(filelist[y].split()[0])+2].split()[1] and \
                            ex_dihs[x][2] == filelist[int(filelist[y].split()[1])+2].split()[1] and \
                            ex_dihs[x][1] == filelist[int(filelist[y].split()[2])+2].split()[1] and \
                            ex_dihs[x][0] == filelist[int(filelist[y].split()[3])+2].split()[1]):
                            if ex_dihs[x][4] != '1' or '4':
                                ex_dihs[x].append('')
                            filelist.insert(y, '%7s  %7s  %7s  %7s  %7s  %7s  %7s  %7s\n' \
                                    %(filelist[y].split()[0],filelist[y].split()[1],\
                                    filelist[y].split()[2],filelist[y].split()[3],\
                                        ex_dihs[x][4],ex_dihs[x][5],ex_dihs[x][6],ex_dihs[x][7]))
                            filelist.pop(y + 1)

    # adding new dihedrals to file list
    try:
        with open('../data/new_dihedrals_parameters.txt') as f:
            f.readlines()
    except FileNotFoundError or NameError:
        pass
    else:
        with open('../data/new_dihedrals_parameters.txt') as f:
            dihedral_types = f.readlines()
        dih_list = []
        # finding new dihedrals which have reacting beads as two terminated beads
        for l in range(len(bonds_found2)):
            one, two, three, four = 0,0,0,0
            if bonds_found2[l][0] in marked_beads:
                four = bonds_found2[l][1]
                three = bonds_found2[l][0]
            else:
                four = bonds_found2[l][0]
                three = bonds_found2[l][1]
            for x in range(len(bonds_found)):
                if bonds_found[x][0] == three:
                    two = bonds_found[x][1]
                    break
                elif bonds_found[x][1] == three:
                    two = bonds_found[x][0]
                    break
            for x in range(len(items)):
                if items[x][0] == two:
                    one = items[x][1]
                    break
                elif items[x][1] == two:
                    one = items[x][0]
                    break
            if (one and two and three and four) != 0:
                dih_list.append((one,two,three,four))
        # finding new dihedrals which have reacting beads in the middle
        for l in range(len(bonds_found)):
            one, two, three, four = 0,0,0,0
            if bonds_found[l][0] in marked_beads:
                four = bonds_found[l][0]
                three = bonds_found[l][1]
            else:
                four = bonds_found[l][1]
                three = bonds_found[l][0]
            for x in range(len(items)):
                if items[x][0] == three:
                    two = items[x][1]
                    break
                elif items[x][1] == three:
                    two = items[x][0]
                    break
            for x in range(len(bonds_found)):
                if bonds_found[x][0] == two:
                    one = bonds_found[x][1]
                elif bonds_found[x][1] == two:
                    one = bonds_found[x][0]
                if (one and two and three and four) != 0:
                    dih_list.append((one,two,three,four))

        for c in range(len(dihedral_types)):
            dih = dihedral_types[c].split()
            if dih ==[]:
                pass
            elif len(dih) not in [7,8]:
                print('Wrong input dihedrals')
                break

        l_count = 0
        for l in range(len(dih_list)):
            first  = filelist[int(dih_list[l][0]) + 2].split()[1]
            second = filelist[int(dih_list[l][1]) + 2].split()[1]
            third  = filelist[int(dih_list[l][2]) + 2].split()[1]
            fourth = filelist[int(dih_list[l][3]) + 2].split()[1]
            dih_type, dih_eq, dih_const, dih_mul = 1,0,0,0
            for c in range(len(dihedral_types)):
                dih = dihedral_types[c].split()
                if dih ==[]:
                    pass
                elif (first == dih[0] and second == dih[1] and third == dih[2] and fourth == dih[3]) or \
                    (first == dih[3] and second == dih[2] and third == dih[1] and fourth == dih[0]):
                    dih_type = dih[4]
                    dih_eq = dih[5]
                    dih_const = dih[6]
                    if dih_type == '1' or '4':
                        dih_mul = dih[7]
                    else:
                        dih_mul = ''
            if (dih_eq and dih_const) != 0 and (len({dih_list[l][0], dih_list[l][1], dih_list[l][2], dih_list[l][3]}) == 4):
                filelist.insert(insert_point+l_count+bond_nos+counter, '%7s  %7s  %7s  %7s  %7s  %7s  %7s  %7s\n' \
                        %(dih_list[l][0], dih_list[l][1], dih_list[l][2], dih_list[l][3], dih_type, dih_eq, dih_const,dih_mul))
                if filelist[insert_point+l_count+bond_nos+counter] == filelist[insert_point+l_count+bond_nos+counter-1]:
                    filelist.pop(insert_point+l_count+bond_nos+counter)
                else:
                    l_count += 1
            else:
                try:   # write undefined dihedrals into a new file for user 
                    with open('../undefined_dihedrals.txt') as g:
                        g.readline()
                except FileNotFoundError or NameError:
                    with open('../undefined_dihedrals.txt', 'w') as g:
                        if len({dih_list[l][0], dih_list[l][1], dih_list[l][2], dih_list[l][3]}) == 4:
                            g.write('%7s (%7s) %7s (%7s) %7s (%7s) %7s (%7s) \n' \
                                    %(dih_list[l][0], first, dih_list[l][1], second, \
                                      dih_list[l][2], third, dih_list[l][3], fourth))
                else:
                    with open('../undefined_dihedrals.txt', 'a') as g:
                        if len({dih_list[l][0], dih_list[l][1], dih_list[l][2], dih_list[l][3]}) == 4:
                            g.write('%7s (%7s) %7s (%7s) %7s (%7s) %7s (%7s) \n' \
                                    %(dih_list[l][0], first, dih_list[l][1], second, \
                                      dih_list[l][2], third, dih_list[l][3], fourth))
    
        # delete duplicates in new dihedrals
        delete = set() # used set instead of list to not keep duplicates
        # check for dihedrals that are same
        for l in range(insert_point+bond_nos+counter,insert_point+l_count+bond_nos+counter):
            d1 = filelist[l].split()
            for x in range(l+1,insert_point+l_count+bond_nos+counter):
                d2 = filelist[x].split()
                if (d1[0] == d2[3] and d1[1] == d2[2] and d1[2] == d2[1] and d1[3] == d2[0]):
                    delete.add(x) # set of repetitious dihedrals which should be deleted
                if (d1[0] == d2[0] and d1[1] == d2[1] and d1[2] == d2[2] and d1[3] == d2[3]):
                    delete.add(x) # set of repetitious dihedrals which should be deleted
        delete = list(delete)
        delete.sort()
        delete.reverse()
        for l in range(len(delete)):
            filelist.pop(delete[l])
    
    if br != []:
        i, bond_line, angle_line, dihedral_line, constraint_line, virtual_line, \
            exclusion_line = 0,0,0,0,0,0,0
        for line in filelist:
            if '[ bonds ]' in line:
                bond_line = i
            if '[ angles ]' in line:
                angle_line = i
            if '[ dihedrals ]' in line and dihedral_line == 0:
                dihedral_line = i
            if '[ constraints ]' in line:
                constraint_line = i
            if '[ virtual_sitesn ]' in line:
                virtual_line = i
            if '[ exclusions ]' in line:
                exclusion_line = i
            i += 1
        end_line = i - 1
        
        br_ind = []   # list containing atoms of breaking bonds
        br_index = []
        del_list = []  # list containing line no.s that should be deleted
        
        if bond_line != 0:
            j = bond_line
            while ('[' not in filelist[j+1]) and (j+1 != end_line+1):
                for k in range(len(br)):
                    if (filelist[int(filelist[j+1].split()[0])+2].split()[4] == br[k][0] and \
                        filelist[int(filelist[j+1].split()[1])+2].split()[4] == br[k][1]) or \
                       (filelist[int(filelist[j+1].split()[0])+2].split()[4] == br[k][1] and \
                        filelist[int(filelist[j+1].split()[1])+2].split()[4] == br[k][0]):
                        if random() <= float(br[k][2]):
                            del_list.append(j+1)
                            br_index.append(filelist[j+1].split()[0])
                            br_index.append(filelist[j+1].split()[1])
                            br_ind.append({filelist[j+1].split()[0],filelist[j+1].split()[1]})
                j += 1
            
        if constraint_line != 0:
            j = constraint_line
            while ('[' not in filelist[j+1]) and (j+1 != end_line+1):
                for k in range(len(br)):
                    if (filelist[int(filelist[j+1].split()[0])+2].split()[4] == br[k][0] and \
                        filelist[int(filelist[j+1].split()[1])+2].split()[4] == br[k][1]) or \
                       (filelist[int(filelist[j+1].split()[0])+2].split()[4] == br[k][1] and \
                        filelist[int(filelist[j+1].split()[1])+2].split()[4] == br[k][0]):
                        if random() <= float(br[k][2]):
                            del_list.append(j+1)
                            br_index.append(filelist[j+1].split()[0])
                            br_index.append(filelist[j+1].split()[1])
                            br_ind.append({filelist[j+1].split()[0],filelist[j+1].split()[1]})
                j += 1
        
        with open('../last_broken_bonds.txt', 'w') as f:
            for j in range(len(del_list)):
                f.write('%-7s   %-7s \n' %(filelist[del_list[j]].split()[0], filelist[del_list[j]].split()[1]))
        
        if angle_line != 0:
            j = angle_line
            while ('[' not in filelist[j+1]) and (j+1 != end_line+1):
                aa = {filelist[j+1].split()[0],filelist[j+1].split()[1],filelist[j+1].split()[2]}
                for k in range(len(br_ind)):
                    if len(aa.intersection(br_ind[k])) == 2:
                        del_list.append(j+1)
                j += 1
        
        if dihedral_line != 0:
            j = dihedral_line
            while ('[' not in filelist[j+1]) and (j+1 != end_line+1):
                aa = {filelist[j+1].split()[0],filelist[j+1].split()[1],filelist[j+1].split()[2],filelist[j+1].split()[3]}
                for k in range(len(br_ind)):
                    if len(aa.intersection(br_ind[k])) == 2:
                        del_list.append(j+1)
                j += 1
        
        if exclusion_line != 0:
            j = exclusion_line
            while ('[' not in filelist[j+1]) and (j+1 != end_line):
                aa = set()
                for k in range(len(filelist[j+1].split())):
                    aa.add(filelist[j+1].split()[k])
                for k in range(len(br_ind)):
                    if len(aa.intersection(br_ind[k])) == 2:
                        del_list.append(j+1)
                j += 1
        
        del_list.sort()
        del_list.reverse()
        for j in del_list:
            filelist.pop(j)
        
        # edit .gro file
        with open(gro_filename , 'r+') as f:
            f.readline() # pass the first two lines of .gro file
            f.readline()
            counter = f.tell() # starting point for bead lines
            for k in range(len(br_index)):
                f.seek(counter+10+45*(int(br_index[k])-1)) # position of the bead name
                sp = f.readline().split()
                f.seek(counter+10+45*(int(br_index[k])-1))
                # check if the bead had been reacted in previous steps (for beads that can react more than one time)
                if sp[0][0] == '1':
                    new_bead_name = sp[0][1:]
                    if (int(br_index[k]) > 9999) and (int(br_index[k]) < 100000):
                        new_bead_name = new_bead_name[:-5]
                    f.write('%5s' %(new_bead_name))
                elif sp[0][0] == '2':
                    new_bead_name = '1'+sp[0][1:]
                    if (int(br_index[k]) > 9999) and (int(br_index[k]) < 100000):
                        new_bead_name = new_bead_name[:-5]
                    f.write('%5s' %(new_bead_name))
                elif sp[0][0] == '3':
                    new_bead_name = '2'+sp[0][1:]
                    if (int(br_index[k]) > 9999) and (int(br_index[k]) < 100000):
                        new_bead_name = new_bead_name[:-5]
                    f.write('%5s' %(new_bead_name))
                elif sp[0][0] == '4':
                    new_bead_name = '3'+sp[0][1:]
                    if (int(br_index[k]) > 9999) and (int(br_index[k]) < 100000):
                        new_bead_name = new_bead_name[:-5]
                    f.write('%5s' %(new_bead_name))
        
        # edit .itp file
        # edit [atoms] section of itp file
        for l in range(len(br_index)):
            line = filelist[int(br_index[l])+2].split()
            if len(line) == 7:
                section_format = table_format_string7
            elif len(line) == 8:
                section_format = table_format_string8
            if line[4][0] == '1': # if the bead is reacting for second time(for beads that can react more than one time)
                filelist.insert(int(br_index[l])+2, section_format %(line[0],line[1],line[2],line[3],line[4][1:],*line[5:len(line)],))
            elif line[4][0] == '2': # if the bead is reacting for third time(for beads that can react more than one time)
                filelist.insert(int(br_index[l])+2, section_format %(line[0],line[1],line[2],line[3],'1'+line[4][1:],*line[5:len(line)],))
            elif line[4][0] == '3': # if the bead is reacting for second time(for beads that can react more than one time)
                filelist.insert(int(br_index[l])+2, section_format %(line[0],line[1],line[2],line[3],'2'+line[4][1:],*line[5:len(line)],))
            elif line[4][0] == '4': # if the bead is reacting for second time(for beads that can react more than one time)
                filelist.insert(int(br_index[l])+2, section_format %(line[0],line[1],line[2],line[3],'3'+line[4][1:],*line[5:len(line)],))
            filelist.pop(int(br_index[l])+3)


    # write the edited file list to itp file
    with open(itp_filename , 'w') as f:
        f.writelines(filelist)

if __name__ == '__main__':
    import sys
    edit_gro_itp(*sys.argv[1:])
