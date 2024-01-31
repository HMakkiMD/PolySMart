"""
Find the distance between atom pairs from two input indices (.txt file)
and make an output file (XL.txt) containing pairs that have the distance
lower than a maximum and higher than a minimum.

How to run:
    > python3 find_distance.py 'filename'.gro 'bead name1'.txt 'bead name2'.txt 'min_distance' 'max_distance' 'probability' 'output.txt'
31.01.2024
"""
import math
from random import random

def find_distance(filename, file1, file2, minimum, maximum, prob, out_path):
    with open(file1) as f:
        list1 = f.readlines()
    if file1[:3] == '../':
        file1 = file1[3:]
    with open(file2) as f:
        list2 = f.readlines()        
    if file2[:3] == '../':
        file2 = file2[3:]
    # check if the input filename has '.gro' or not
    if filename[-4:] != '.gro':
        filename += '.gro'

    with open(filename) as f:
        filelist = f.readlines()        
        with open(out_path[:-4]+'_noprob.txt', 'w') as g: # output_noprob.txt is the output containing bead pairs before applying probability
            pass
        with open(out_path, 'w') as g: # output.txt is the output containing bead pairs
            pass

        for i in range(len(list1)):
            line1 = filelist[int(list1[i])+1] # line attributed to bead no. i
            coord1 = (float(line1[20:28]), float(line1[28:36]), float(line1[36:44]))
            if file1 == file2:
                beg = i + 1
            else:
                beg = 0
            for j in range(beg, len(list2)):
                line2 = filelist[int(list2[j])+1] # line attributed to bead no. j
                if line1[:5] != line2[:5]:
                    # find coordinates of 2 beads and calculate the distance between them
                    coord2 = (float(line2[20:28]), float(line2[28:36]), float(line2[36:44]))
                    dist = math.sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2+(coord1[2]-coord2[2])**2)
                    if dist < maximum and dist > minimum: # check if the distance is in desired range
                        with open(out_path[:-4]+'_noprob.txt', 'a') as g:
                            g.write('%-7s\t %7s\t %-7s\t %7s\t %8.5f\n' %(file1[:-4], int(list1[i]), file2[:-4], int(list2[j]), dist))
                        with open(out_path, 'a') as g:
                            if random() <= prob:
                                g.write('%-7s\t %7s\t %-7s\t %7s\t %8.5f\n' %(file1[:-4], int(list1[i]), file2[:-4], int(list2[j]), dist))

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    file1 = sys.argv[2] # bead 1 indices
    file2 = sys.argv[3] # bead 2 indices
    minimum = float(sys.argv[4]) # minimum distance betwwen beads for reaction
    maximum = float(sys.argv[5]) # maximum distance betwwen beads for reaction
    prob = float(sys.argv[6]) # probability of find for reaction
    out_path = sys.argv[7]
    find_distance(filename, file1, file2, minimum, maximum, prob, out_path)
