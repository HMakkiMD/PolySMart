"""
Pre-run before entering the crosslinking loops. Making new itp files, subfolders and first relaxation step

11.03.2022
"""

import os

# read lines of input.txt and assign parameters
with open('../data/inputs.txt') as f:
    l = f.readlines()
    for i in range(len(l)):
        l[i] = l[i].split()
    begin_loop = int(l[0][0])
    threads = l[0][1]
    cycles = int(l[0][2])
    conv = float(l[0][3])
    ref_conv_bead = l[0][4]
    types = len(l[1])

    reactant_bead = []
    reactant_bead_no = []
    # define all possible reactive beads based on their reactivity
    for i in range(len(l[3])//2):
        reactant_bead.append(l[3][2*i])
        reactant_bead_no.append(l[3][2*i+1])
    no_of_beads = len(reactant_bead_no)
    for i in range(no_of_beads):
        for j in range(2,5):
            if reactant_bead_no[i] == str(j):
                for k in range(1,j):
                    reactant_bead.append(str(k)+reactant_bead[i])
                    reactant_bead_no.append(str(j-k))

conversion = []
n = []
for i in range(len(l[3])//2):
    conversion.append(0.0000)
    n.append(0)
    # find that which index is attributed to reference bead for calculating conversion
    if l[3][2*i] == ref_conv_bead:
        ref_index = i

# modify input itp files with it_modify.py
from itp_modify import itp_modify
for i in range(types):
    itp_modify(f'../data/{l[1][i]}')
# produce merged itp file
from itp_merge import itp_merge
itp_merge(types, ['../data/'+str(f[:-4])+'_modified' for f in l[1]], list(int(f) for f in l[2]), '../product.itp')

os.system(f'sh pre_relax.sh {threads}')

# make all_loops.txt which include all reaction during loops
with open('../loops/all_loops.txt', 'w') as f:
    f.write('')

with open('../conversion.xvg', 'w') as f:
    f.write('@    title "Conversion"\n')
    f.write('@    xaxis  label "loops (number)"\n')
    f.write('@    yaxis  label "Percentage"\n')
    f.write('@TYPE xy\n')
    f.write('@ view 0.15, 0.15, 0.75, 0.85\n')
    f.write('@ legend on\n')
    f.write('@ legend box on\n')
    f.write('@ legend loctype view\n')
    f.write('@ legend 0.78, 0.8\n')
    f.write('@ legend length 2\n')
    for i in range(len(l[3])//2):
        f.write(f'@ s{i} legend "{reactant_bead[i]}"\n')
    f.write('%7d ' %(0))
    for i in range(len(l[3])//2):
        f.write('%8.4f ' %(0))
    f.write('\n')
