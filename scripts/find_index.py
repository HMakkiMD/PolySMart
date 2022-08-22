"""
Find indices of an input bead name from input gro file,
and make new file named 'beadname.txt' containing indices.

How to run:
    > python3 find_index.py 'filename'.gro 'Your bead name' 'reaction_capacity'    
11.03.2022
"""

def find_index(filename, index, reaction_capacity):
    with open(filename) as f:
        l = f.readlines()
        with open('../'+index+'.txt', 'w') as g:
            for i in range(2,len(l)):
                st = l[i].split()
                if (i > 10000) and (i < 100001):
                    temp = st.copy()
                    st[1], st[2] = temp[1][:-5], temp[1][-5:]
                if reaction_capacity == 1:
                    if index in st:
                        g.write(f'{i-1}\n')
                elif reaction_capacity == 2:
                    if (index in st) or ('1'+index in st):
                        g.write(f'{i-1}\n')
                elif reaction_capacity == 3:
                    if (index or '1'+index or '2'+index) in st:
                        g.write(f'{i-1}\n')
                elif reaction_capacity == 4:
                    if (index or '1'+index or '2'+index or '3'+index) in st:
                        g.write(f'{i-1}\n')

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    index = sys.argv[2]
    reaction_capacity = int(sys.argv[3])
    find_index(filename, index, reaction_capacity)
