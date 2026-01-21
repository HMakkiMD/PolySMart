clc; clear; close all;
system('python gMBCP_clusters.py');
LC = xlsread('gmbcp_clusters.xlsx');
LC_bead_No = LC;%(:,1);
Length_LC=size(LC_bead_No,1);
num_cluster = size(LC,2);

bead_number_each_cluster = sum(LC ~= 0);

mw_bead = floor(sum(bead_number_each_cluster.^2)/(sum(bead_number_each_cluster)));
size=mean(mw_bead)/120 %change the number based on the average beads of the system
fileID = fopen('size of gmbcp.txt','w');
fprintf(fileID, '%f\n', size);
fclose(fileID);