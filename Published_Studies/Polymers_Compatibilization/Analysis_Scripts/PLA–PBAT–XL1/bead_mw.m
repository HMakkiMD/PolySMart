clc; clear; close all;
tic
files = dir('loop*.xlsx');
loop = '';
network = '';
if isempty(files)
    disp('No matching file found.');
else
    loop = files(1).name;
    disp(['loop: ' loop]);
    numberStr = regexpi(loop, 'loop(\d+)\.xlsx', 'tokens', 'once');
    
    if ~isempty(numberStr)
        % Construct the new variable 'a'
        network = ['network' numberStr{1} '.xlsx'];
        disp(['netwrok: ' network]);
    else
        disp('No number found in the filename.');
    end
end

filename_input = loop;
filename_output = network;

filename = filename_output;
sheet = 'histogram-matrix';
LC = xlsread(filename,sheet);
LC_bead_No = LC;%(:,1);
Length_LC=size(LC_bead_No,1);
num_cluster = size(LC,2);

bead_number_each_cluster = sum(LC ~= 0);

mn_bead = sum(bead_number_each_cluster)/size(bead_number_each_cluster,2);
mw_bead = floor(sum(bead_number_each_cluster.^2)/(sum(bead_number_each_cluster)));
PDI_bead = mw_bead/mn_bead;
xlswrite('analysis.xlsx',mw_bead,'PDI_bead','A1');
xlswrite('analysis.xlsx',mn_bead,'PDI_bead','B1');
xlswrite('analysis.xlsx',PDI_bead,'PDI_bead','C1');