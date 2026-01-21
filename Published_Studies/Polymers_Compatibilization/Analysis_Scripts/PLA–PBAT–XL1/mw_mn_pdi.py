import os
import re
import pandas as pd
import numpy as np
import time

start_time = time.time()

# Find the file starting with "loop" and ending in ".xlsx"
files = [f for f in os.listdir() if f.startswith("loop") and f.endswith(".xlsx")]
loop = ''
network = ''

if not files:
    print("No matching file found.")
else:
    loop = files[0]
    print(f"Matching file found: {loop}")
    match = re.search(r'loop(\d+)\.xlsx', loop)
    if match:
        number = match.group(1)
        network = f'network{number}.xlsx'
        print(f"New variable a: {network}")
    else:
        print("No number found in the filename.")

filename_input = loop
filename_output = network

# Read histogram matrix
hist_sheet = 'histogram-matrix'
LC_df = pd.read_excel(filename_output, sheet_name=hist_sheet, header=None)
LC_bead_No = LC_df.values
Length_LC, num_cluster = LC_bead_No.shape

# Read atoms sheet
atoms_df = pd.read_excel(filename_input, sheet_name=' atoms ', header=None)
atoms = atoms_df.values
all_bead_no = atoms[:, 0].astype(int)

# Define molar masses for each bead
mass_dict = {
    'COOH': 45.02, 'CCH3': 28.05, 'PCOO': 44.1, '1CCH3': 27.05, 'CCOH': 45.06,
    'COH': 29.02, 'C2H1': 25.03, 'C2H2': 26.04, 'COO': 44.01, 'CCH4': 28.05, '1CCH4': 27.05,
    'CF3': 71.0, 'C2H2': 26.0, 'COC': 40.0, '1COO': 44.0, 'COCC': 52.0, 'DAZ': 64.0, '1DAZ': 37.0
}

MM = np.zeros(num_cluster)

# Calculate molecular weight of each cluster
for m in range(num_cluster):
    for k in range(Length_LC):
        bead = LC_bead_No[k, m]
        if bead != 0:
            match_indices = np.where(all_bead_no == bead)[0]
            for i in match_indices:
                group = str(atoms[i, 4]).strip()
                MM[m] += mass_dict.get(group, 0)

# Sort and calculate Mn, Mw, PDI
MM = np.sort(MM)
mn = np.sum(MM) / len(MM)
mw = np.floor(np.sum(MM**2) / np.sum(MM))
PDI = mw / mn

# Save results to Excel
df_out = pd.DataFrame([[mw, mn, PDI]], columns=['Mw', 'Mn', 'PDI'])
with pd.ExcelWriter('analysis_mw.xlsx', engine='openpyxl') as writer:
    df_out.to_excel(writer, sheet_name='PDI', index=False, startrow=0, startcol=0)

print("Execution time: {:.2f} seconds".format(time.time() - start_time))
