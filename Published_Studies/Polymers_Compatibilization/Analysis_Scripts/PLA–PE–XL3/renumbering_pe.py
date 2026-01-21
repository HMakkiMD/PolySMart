# -*- coding: utf-8 -*-
"""
how to run :
    python3   renumbering.py   [itp file name]
    
Created on Fri Feb 23 14:19:53 2024

@author: Mohammad
"""

import glob
import sys

itp_files = glob.glob('*.itp')

if not itp_files:
    print("No .itp file found.")
    sys.exit(1)

file_name = itp_files[0]

if file_name.endswith('.itp'):
    file_name = file_name[:-4]

print(f"Selected file (without extension): {file_name}")

exchanges_yes = []
exchanges_no = []

# detect the exchanged bonds
with open(f'{file_name}.itp') as f:
    lines = f.readlines()
    for line in lines:
        if '100000' in line.split() and ('0.243' or '0.245') in line.split():
            exchanges_yes.append([line.split()[0],line.split()[1]])
        if '1000000' in line.split() and ('0.243' or '0.245') in line.split():
            exchanges_no.append([line.split()[0],line.split()[1]])
# sort the exchanges in a way that first beads have not same molecule numbers
exchanges = exchanges_yes + exchanges_no
temp = ''
x = 0
'''
for i in range(len(exchanges)):
    if exchanges[i][1] < exchanges[i][0]:
        temp = exchanges[i][0]
        exchanges[i][0] = exchanges[i][1]
        exchanges[i][1] = temp
exchanges.sort()

'''
for i in range(len(exchanges)):
    for j in range(i+1,len(exchanges)):
        if lines[int(exchanges[i][0])+2].split()[2] == lines[int(exchanges[j][0])+2].split()[2]:
            temp = exchanges[j][0]
            exchanges[j][0] = exchanges[j][1]
            exchanges[j][1] = temp
            x += 1

# exchange molecule numbers
new_num = 5000
for i in exchanges:
    #new_num = lines[int(i[0])+2].split()[2]
    if lines[int(i[0])+2].split()[3] == 'UDC':
        y = 5
    elif lines[int(i[0])+2].split()[3] == 'CLD':
        y = 9
    if lines[int(i[0])+2].split()[1] == lines[int(i[0])+3].split()[1]:
        for j in range (y):
            lines[int(i[0])+2-j] = '%7s\t %-7s%6s   %-5s  %-6s  %7s   %-5s\n' \
            %(lines[int(i[0])+2-j].split()[0],lines[int(i[0])+2-j].split()[1],new_num,\
            lines[int(i[0])+2-j].split()[3],lines[int(i[0])+2-j].split()[4],\
            lines[int(i[0])+2-j].split()[5],lines[int(i[0])+2-j].split()[6])
    else:
        for j in range (y):
            lines[int(i[0])+2+j] = '%7s\t %-7s%6s   %-5s  %-6s  %7s   %-5s\n' \
            %(lines[int(i[0])+2+j].split()[0],lines[int(i[0])+2+j].split()[1],new_num,\
            lines[int(i[0])+2+j].split()[3],lines[int(i[0])+2+j].split()[4],\
            lines[int(i[0])+2+j].split()[5],lines[int(i[0])+2+j].split()[6])
    
    if lines[int(i[1])+2].split()[1] == lines[int(i[1])+3].split()[1]:
        for j in range (y):
            lines[int(i[1])+2-j] = '%7s\t %-7s%6s   %-5s  %-6s  %7s   %-5s\n' \
            %(lines[int(i[1])+2-j].split()[0],lines[int(i[1])+2-j].split()[1],new_num,\
            lines[int(i[1])+2-j].split()[3],lines[int(i[1])+2-j].split()[4],\
            lines[int(i[1])+2-j].split()[5],lines[int(i[1])+2-j].split()[6])
    else:
        for j in range (y):
            lines[int(i[1])+2+j] = '%7s\t %-7s%6s   %-5s  %-6s  %7s   %-5s\n' \
            %(lines[int(i[1])+2+j].split()[0],lines[int(i[1])+2+j].split()[1],new_num,\
            lines[int(i[1])+2+j].split()[3],lines[int(i[1])+2+j].split()[4],\
            lines[int(i[1])+2+j].split()[5],lines[int(i[1])+2+j].split()[6])

    new_num += 1
# write modified itp file
with open(f'{file_name}_modified.itp','w') as g:
    g.writelines(lines)


cl_bonds = []
with open(f'{file_name}_modified.itp') as g:
    lines = g.readlines()
    for i in range(len(lines)):
        if 'bonds' in lines[i]:
            bond_line = i
        if 'angles' in lines[i]:
            ang_line = i
# find crosslink bonds
for i in range(bond_line+1,ang_line):
    if lines[i].split()[4] in ['14800','12000']:
        cl_bonds.append([lines[i].split()[0],lines[i].split()[1]])

pe_cls = []   # list of reacted P3HB beads and their molecule number
pla_cls   = []   # list of reacted PE   beads and their molecule number
cl_cls   = []   # list of reacted UDC  beads and their molecule number
for i in range(3,bond_line):
    if lines[i].split()[4] == '1C2H4':
        pe_cls.append([lines[i].split()[0],lines[i].split()[2]])
    elif lines[i].split()[4] == '1CCH3':
        pla_cls.append([lines[i].split()[0],lines[i].split()[2]])
    elif lines[i].split()[4] == '1DAZ':
        cl_cls.append([lines[i].split()[0],lines[i].split()[2]])

# find molecules that are connected to each other
mol_bonds = []
c = 0
polymer = pe_cls + pla_cls
for i in range(len(cl_bonds)):
    mol1 , mol2 = '',''
    for j in range(len(cl_bonds)):
        if cl_bonds[i][0] == cl_cls[j][0]:
            mol1 = cl_cls[j][1]
        if cl_bonds[i][1] == polymer[j][0]:
            mol2 = polymer[j][1]
            c += 1
            
    if mol1 != '' and mol2 != '':
        mol_bonds.append([mol1,mol2])
    else:
        print('Something is wrong!')

pla_udc_pe , pla_udc_pla , pe_udc_pe , loops, counter = 0,0,0,0,0
pe_mols , pla_mols = [],[]
# find double reacted UDCs and to which polymer they are connected
for i in pe_cls:
    pe_mols.append(i[1])
for i in pla_cls:
    pla_mols.append(i[1])
for i in range(len(mol_bonds)):
    for j in range(i+1,len(mol_bonds)):
        if mol_bonds[i][0] == mol_bonds[j][0]:
            counter += 1
            if mol_bonds[i][1] == mol_bonds[j][1]:
                loops += 1
                #print(mol_bonds[i][0])
            if (mol_bonds[i][1] in pla_mols) and (mol_bonds[j][1] in pla_mols):
                pla_udc_pla += 1
            elif (mol_bonds[i][1] in pe_mols) and (mol_bonds[j][1] in pe_mols):
                pe_udc_pe += 1
            elif ((mol_bonds[i][1] in pla_mols) and (mol_bonds[j][1] in pe_mols)) or \
                 ((mol_bonds[i][1] in pe_mols) and (mol_bonds[j][1] in pla_mols)):
                pla_udc_pe += 1
            #break
'''
a = []
for w in range(5000,5400):
    b = []
    for v in range(800):
        if mol_bonds[v][0] == str(w):
            b.append(mol_bonds[v][1])
    a.append([str(w),b])
'''
    
    
# write the results
with open(f'{file_name}_results.txt','w') as f:
    f.write('|=================================================|\n')
    f.write('|  No. of     PE-CL-PE connections   =   %7d  |\n' %(pe_udc_pe))
    f.write('|  No. of  PLA-CL-PLA  connections   =   %7d  |\n' %(pla_udc_pla))
    f.write('|  No. of   PE-CL-PLA  connections   =   %7d  |\n' %(pla_udc_pe))
    f.write('|  No. of first order loops          =   %7d  |\n' %(loops))
    f.write('|=================================================|\n')