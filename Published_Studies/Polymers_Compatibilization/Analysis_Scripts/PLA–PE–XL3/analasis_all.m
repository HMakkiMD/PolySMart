clc; clear; close all;
tic
system('python itp_excel.py');
files = dir('loop*.xlsx');
loop = '';
network = '';
if isempty(files)
    disp('No matching file found.');
else
    loop = files(1).name;
    disp(['Matching file found: ' loop]);
    numberStr = regexpi(loop, 'loop(\d+)\.xlsx', 'tokens', 'once');
    
    if ~isempty(numberStr)
        network = ['network' numberStr{1} '.xlsx'];
        disp(['New variable a: ' network]);
    else
        disp('No number found in the filename.');
    end
end

filename_input = loop;
filename_output = network;
sheet = 'Bonds_Constraints';
[~, ~, raw] = xlsread(filename_input, sheet);
bonds = str2double(raw);

% Graph
ibonds = size(bonds,1);
jbonds = size(bonds,2);

source_nodes = bonds(:,1);
target_nodes = bonds(:,2);

Z = zeros(ibonds,1);
for i = 1:ibonds
   Z(i) = 1;     
end

edge = Z;

G = graph(source_nodes,target_nodes,edge);
%figure(1);h=plot(G,'Layout','force');

bins = conncomp(G);
bins=bins';
max_bins = max(bins); %number of molecule in box
xsa = size(bins); 
all_bead_No = xsa(1);  %number of beads in box

hist1 = [(1:all_bead_No)' bins]; %each bead number for which cluster
hist2 = sortrows(hist1,2); %sort matrix hist1
hist3 = hist2(:,2);
y = hist(hist3,max_bins); %number of the molecule and number of the beads in it
max_y = max(y);
%hist(hist3,max_bins); 

hist_mat = zeros(max_y,max_bins);
for j=1:max_bins
    c=0;
    for i=1:all_bead_No
        if hist2(i,2)==j
            c=c+1;
            hist_mat(c,j)=hist2(i,1);
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% analysis hist_mat matrix........ hist max is the molecule number and the
% bead number in it

r_hm = size(hist_mat,1); % row number of hist_mat matrix
c_hm = size(hist_mat,2); % column number of hist_mat matrix

N_all = all_bead_No;     % number of all beads
N_C = c_hm;              % number of clusters
N_L_C = r_hm;            % number of beads in largest cluster

P_L_C = (N_L_C/N_all) * 100;     % percent of largest cluster


% bead numbers of each cluster

for i=1:c_hm
    clusters(i,1)=i; % cluster number
    clusters(i,2)=nnz(hist_mat(:,i));  % number of beads in each cluster
    clusters(i,3)=(nnz(hist_mat(:,i))/N_all)*100; % percent of bead number in each cluster
end

max_clusters=max(clusters(:,2));
p_max_clusters=max(clusters(:,3));
mean_clusters=mean(clusters(:,2));
p_mean_clusters=(mean_clusters/N_all)*100;

output=[N_all N_C max_clusters p_max_clusters mean_clusters p_mean_clusters];

% analysis degree of nodes

% find the node numbers of the largest cluster (such as the node numbers of
% longest clusters)

max_clusters = max(clusters(:,2));
%[r_max_histmat,c_max_histmat]=
d=find(clusters(:,2)==max_clusters);
d=d(1);

largest_cluster_nodes=hist_mat(:,d);


% find degree of largest cluster
largest_cluster_degree=degree(G,largest_cluster_nodes);

% largest cluster node number and degree of nodes
largest_cluster_nodes_degree=[largest_cluster_nodes largest_cluster_degree];

% find nodes with 1, 2 and 3 edges
c1=0; c2=0; c3=0;
for i=1:size(largest_cluster_nodes_degree,1)
    if largest_cluster_nodes_degree(i,2)==1
        c1=c1+1;
        L_degree1(c1,1)=largest_cluster_nodes_degree(i,1);
        L_degree1(c1,2)=largest_cluster_nodes_degree(i,2);      
    end
    
    if largest_cluster_nodes_degree(i,2)==2
        c2=c2+1;
        L_degree2(c2,1)=largest_cluster_nodes_degree(i,1);
        L_degree2(c2,2)=largest_cluster_nodes_degree(i,2);      
    end

    if largest_cluster_nodes_degree(i,2)==3
        c3=c3+1;
        L_degree3(c3,1)=largest_cluster_nodes_degree(i,1);
        L_degree3(c3,2)=largest_cluster_nodes_degree(i,2);      
    end
        
end

% difine network index1:
% number of nodes with 1 degree in largest cluster/number of nodes with 3 degree in largest cluster
%cycles8 = allcycles(G, "MaxCycleLength",i, "MinCycleLength",i);

%network_index1=(size(L_degree1,1)/size(L_degree3,1))

%xlswrite(filename_output,{'network index1'},'output','G1');
%xlswrite(filename_output,network_index1,'output','G2');

%xlswrite(filename_output,largest_cluster_nodes_degree,'the longest cluster');


%xlswrite(filename_output,L_degree1,'largest cluster degree1');
%xlswrite(filename_output,L_degree2,'largest cluster degree2');
%xlswrite(filename_output,L_degree3,'largest cluster degree3');

xlswrite(filename_output,hist_mat,'histogram-matrix');
%xlswrite(filename_output,clusters,'clusters with bead number');
%xlswrite(filename_output,output,'output','A2:F2');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bead_mw
system('python analasis_all_pythn.py');
system('python combine_interface_data.py');
system('python mw_mn_pdi.py');
system('python renumbering_pe.py');
size_gmbcp
system('python remove_extra.py');

toc