"""
Run the crosslinking reaction loops from a pre-relaxed structure (after running "run_first_relaxation_only.py")
or resume a crosslinking reaction

if you do not want to run a reaction from the beginning (resume a reaction that has been
stopped) just edit input.txt file

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

os.system('cp ../data/mixture_raw.gro ../md/md0.gro')
# finding the time of run (in ps) for trjconv
with open('../data/martini_run.mdp') as f:
    li = f.readlines()
    for i in range(len(li)):
        if li[i].split() == []:
            pass
        elif li[i].split()[0] == 'dt':
            dt = li[i].split()[2]
        elif li[i].split()[0] == 'nsteps':
            steps = li[i].split()[2]
    time = int(float(dt)*int(steps)) - int(float(dt)*1000)
os.system(f'echo 0 | gmx trjconv -f ../md/md0.xtc -s ../md/md0.tpr -o ../md/md0.gro -b {time} -e {time}')
os.system('rm ../md/#md0.gro.1#')
# find the maximum number of reactions that can be done for each reactive bead (for calculating conversion)
from find_index import find_index

for i in range(len(reactant_bead)):
    find_index('../md/md0.gro', f'{reactant_bead[i]}', 1)
max_reactions = []
for i in range(len(l[3])//2):
    with open(f'../{reactant_bead[i]}.txt') as f:
        max_reactions.append(int(len(f.readlines()))*int(reactant_bead_no[i]))

# finding the time of equlibration in loops (in ps) for trjconv
with open('../data/martini_eqxl.mdp') as f:
    le = f.readlines()
    for i in range(len(le)):
        if le[i].split() == []:
            pass
        elif le[i].split()[0] == 'dt':
            dt = le[i].split()[2]
        elif le[i].split()[0] == 'nsteps':
            steps = le[i].split()[2]
    time = int(float(dt)*int(steps)) - int(float(dt)*1000)

# editing all_loops.txt and conversion.xvg in case you start the loops again from some previous loops
try:
    with open(f'../loops/loop{begin_loop}.txt') as f:
        first_line = f.readline()
except FileNotFoundError or NameError:
    pass
else:
    with open('../loops/all_loops.txt') as g:
        reactions = g.readlines()
    for j in range(len(reactions)):
        if reactions[j] == first_line:
            for k in range(len(reactions)-1, j-1, -1):
                reactions.pop()
            break
    with open('../loops/all_loops.txt', 'w') as g:
        g.writelines(reactions)
    with open('../conversion.xvg') as g:
        reactions = g.readlines()
    for j in range(len(reactions)-1, 10, -1):
        try:
            int(reactions[j].split()[0])
        except ValueError:
            pass
        else:
            if int(reactions[j].split()[0]) >= begin_loop:
                reactions.pop()
    with open('../conversion.xvg', 'w') as g:
        g.writelines(reactions)

i = begin_loop
# crosslinking loops
from find_distance import find_distance
while conversion[ref_index] < conv:
    # find all reacting beads in the system
    for j in range(len(reactant_bead)):
        find_index(f'../md/md{i-1}.gro', f'{reactant_bead[j]}', 1)

    os.system(f'sh edit_files.sh {i} {time}')
        
    # find distances for all reacting beads
    for j in range(4, len(l)):
        inp = l[j]
        find_distance(f'../md/md{i-1}.gro', f'../{inp[0]}.txt', f'../{inp[1]}.txt', float(inp[2]), float(inp[3]), float(inp[4]), '../XL.txt')
        if len(l) > 5:
            os.system(f'cp ../XL.txt ../XL_temp{j-3}.txt')
            if j == len(l)-1:
                with open('../XL.txt' , 'w') as f:
                    for k in range(1, len(l)-3):
                        with open(f'../XL_temp{k}.txt') as g:
                            temp = g.readlines()
                        f.writelines(temp)
    if len(l) > 5:
        for j in range(1, len(l)-3):
            os.system(f'rm ../XL_temp{j}.txt')

    # edit .gro and .itp files after reaction
    from edit_gro_itp import edit_gro_itp
    os.system(f'cp ../md/md{i-1}.gro ../md/temp.gro')
    edit_gro_itp('../XL.txt', f'../md/md{i-1}.gro', '../product.itp', f'../loops/loop{i}.txt')
    # run the relaxation step
    os.system(f'sh post_relax.sh {i-1} {threads} {time}')
    os.system(f'../md/temp.gro cp ../md/md{i-1}.gro')
    os.system('rm ../md/temp.gro')
    
    # find the number of reactions took place so far, and calculate the conversion
    with open(f'../loops/loop{i}.txt') as f:
        with open('../loops/all_loops.txt', 'a') as g:
            ls = f.readlines()
            g.writelines(ls)
        with open('../loops/all_loops.txt') as g:
            co = g.readlines()
        for j in range(len(n)):
            n[j] = 0
        for j in range(len(co)):
            for k in range(len(n)):
                if (reactant_bead[k] in co[j].split()) or \
                    ('1'+reactant_bead[k] in co[j].split()) or \
                        ('2'+reactant_bead[k] in co[j].split()) or \
                            ('3'+reactant_bead[k] in co[j].split()):
                    n[k] += 1

    for j in range(len(n)):
        try:
            conversion[j] = n[j]/max_reactions[j]*100
        except ZeroDivisionError:
            conversion[j] = 0
        else:
            conversion[j] = n[j]/max_reactions[j]*100
    with open(f'../loops/loop{i}.txt', 'a') as f:
        f.write(f'Conversion = {conversion[ref_index]} %')

    # make xvg file for plotting conversion
    with open('../conversion.xvg', 'a') as f:
        f.write('%7d ' %(i))
        for j in range(len(n)):
            f.write('%8.4f ' %(conversion[j]))
        f.write('\n')

    if i == cycles:
        break
    else:
        i += 1
