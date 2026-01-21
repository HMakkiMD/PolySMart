"""
Find indices of an input bead name from input gro file,
and make new file named 'beadname.txt' containing indices.

How to run:
    > python3 find_index.py 'filename'.gro 'Your bead name' 'reaction_capacity'    
31.01.2024
"""

def find_index(filename, index, reaction_capacity):
    with open(filename) as f:
        l = f.readlines()
        with open('../'+index+'.txt', 'w') as g:
            for i in range(2,len(l)):
                if reaction_capacity == 1:
                    if index == l[i][10:15].split()[0]:
                        g.write(f'{i-1}\n')
                elif reaction_capacity == 2:
                    if l[i][10:15].split()[0] in [index,'1'+index]:
                        g.write(f'{i-1}\n')
                elif reaction_capacity == 3:
                    if l[i][10:15].split()[0] in [index,'1'+index,'2'+index]:
                        g.write(f'{i-1}\n')
                elif reaction_capacity == 4:
                    if l[i][10:15].split()[0] in [index,'1'+index,'2'+index,'3'+index]:
                        g.write(f'{i-1}\n')

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    index = sys.argv[2]
    reaction_capacity = int(sys.argv[3])
    find_index(filename, index, reaction_capacity)
