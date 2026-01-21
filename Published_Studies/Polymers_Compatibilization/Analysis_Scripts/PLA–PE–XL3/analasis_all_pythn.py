import pandas as pd
import numpy as np
import os
import time
import re

start_time = time.time()

# === Auto-detect file numbers ===
loop_file = None
network_file = None
loop_number = None

for f in os.listdir('.'):
    if f.startswith('loop') and f.endswith('.xlsx'):
        loop_file = f
        match = re.search(r'loop(\d+)\.xlsx', f)
        if match:
            loop_number = match.group(1)
        break

if loop_number:
    for f in os.listdir('.'):
        if f.startswith('network' + loop_number) and f.endswith('.xlsx'):
            network_file = f
            break
else:
    raise FileNotFoundError("No valid loopXX.xlsx file found.")

if not network_file:
    raise FileNotFoundError(f"No matching network{loop_number}.xlsx file found.")

# === File Names ===
filename_output = network_file
filename_input = loop_file





# === Load Data ===
LC = pd.read_excel(filename_output, sheet_name='histogram-matrix', header=None).values
Length_LC, num_cluster = LC.shape
atoms = pd.read_excel(filename_input, sheet_name=' atoms ', header=None).values
all_bead_no = atoms[:, 0].astype(str).astype(int)

# === Utility Function to Process Clusters ===
def process_cluster(bead_type_index, bead_type_name):
    rep = np.zeros((Length_LC, num_cluster))
    for m in range(num_cluster):
        for k in range(Length_LC):
            bead_id = LC[k, m]
            if bead_id != 0:
                matches = np.where(all_bead_no == bead_id)[0]
                for i in matches:
                    if str(atoms[i, bead_type_index]) == bead_type_name:
                        rep[k, m] = float(atoms[i, 2])
    return rep

def clean_and_sort(rep):
    cleaned = rep.copy()
    for col in range(rep.shape[1]):
        col_vals = rep[:, col]
        nonzero_vals = col_vals[col_vals != 0]
        unique_vals = np.unique(nonzero_vals)
        if len(unique_vals) < len(nonzero_vals):
            cleaned[:, col] = np.nan
            cleaned[:len(unique_vals), col] = unique_vals
    count_per_cluster = np.sum(cleaned > 0, axis=0)
    cluster_ids = np.arange(1, num_cluster + 1)
    result = np.column_stack((cluster_ids, count_per_cluster))
    result = result[result[:, 1] != 0]
    sorted_result = result[np.argsort(-result[:, 1])]
    return sorted_result

# === PLA: 1CCH3 ===
rep_pla = process_cluster(bead_type_index=4, bead_type_name='1CCH3')
sorted_pla = clean_and_sort(rep_pla)
pd.DataFrame(sorted_pla).to_excel('PLA-cluster.xlsx', index=False, header=False)

# === PE: 1C2H4 ===
rep_pbat = process_cluster(bead_type_index=4, bead_type_name='1C2H4')
sorted_pbat = clean_and_sort(rep_pbat)
pd.DataFrame(sorted_pbat).to_excel('PBAT-cluster.xlsx', index=False, header=False)

# === CRE: CLD ===
rep_cre = np.zeros((Length_LC, num_cluster))
for m in range(num_cluster):
    for k in range(Length_LC):
        bead_id = LC[k, m]
        if bead_id != 0:
            matches = np.where(all_bead_no == bead_id)[0]
            for i in matches:
                if str(atoms[i, 3]) == 'UDC':
                    rep_cre[k, m] = int(atoms[i, 0])

count_cre = np.count_nonzero(rep_cre, axis=0) / 10  # replace 10 if needed
cre_result = np.column_stack((np.arange(1, num_cluster + 1), count_cre))
cre_result = cre_result[cre_result[:, 1] != 0]
sorted_cre = cre_result[np.argsort(-cre_result[:, 1])]

if os.path.exists('CRE-cluster.xlsx'):
    os.remove('CRE-cluster.xlsx')
pd.DataFrame(sorted_cre).to_excel('CRE-cluster.xlsx', index=False, header=False)

# === Merge for interface_and_pe.txt ===
p3hb = pd.read_excel('PLA-cluster.xlsx', header=None).values
pe = pd.read_excel('PBAT-cluster.xlsx', header=None).values
cre = pd.read_excel('CRE-cluster.xlsx', header=None).values

chains = np.zeros((pe.shape[0], 4))
for i in range(pe.shape[0]):
    chains[i, 0] = pe[i, 0]
    chains[i, 1] = pe[i, 1]
    match_p3hb = p3hb[p3hb[:, 0] == pe[i, 0]]
    if match_p3hb.shape[0]:
        chains[i, 2] = match_p3hb[0, 1]
    match_cre = cre[cre[:, 0] == pe[i, 0]]
    if match_cre.shape[0]:
        chains[i, 3] = match_cre[0, 1]

chains = chains[np.argsort(-chains[:, 1])]  # sort by PE column (same as MATLAB)
np.savetxt('interface_and_pe.txt', chains[:, 1:], fmt='%.6f')  # drop ID column

# === Merge for p3hb_bulk.txt ===
chains_bulk = []
for i in range(p3hb.shape[0]):
    cluster_id = p3hb[i, 0]
    if cluster_id not in pe[:, 0]:
        entry = [p3hb[i, 1], 0]
        match_cre = cre[cre[:, 0] == cluster_id]
        if match_cre.shape[0]:
            entry[1] = match_cre[0, 1]
        chains_bulk.append(entry)

chains_bulk = np.array(chains_bulk)
np.savetxt('p3hb_bulk.txt', chains_bulk, fmt='%.6f')

# === Run external scripts ===
os.system('python interface_and_pe.py')
os.system('python p3hb_bulk.py')






# === Identify interface clusters ===
rep_pe = np.zeros((Length_LC, num_cluster), dtype=int)
rep_p3hb = np.zeros((Length_LC, num_cluster), dtype=int)

for m in range(num_cluster):
    for k in range(Length_LC):
        bead_id = LC[k, m]
        if bead_id != 0:
            matches = np.where(all_bead_no == bead_id)[0]
            for i in matches:
                if str(atoms[i, 4]).strip() == '1C2H4':
                    rep_pe[k, m] = m + 1  # MATLAB is 1-based
                elif str(atoms[i, 4]).strip() == '1CCH3':
                    rep_p3hb[k, m] = m + 1

# === Get intersecting cluster IDs ===
interface_clusters = sorted(set(rep_pe.flatten()) & set(rep_p3hb.flatten()))
interface_clusters = [cid for cid in interface_clusters if cid != 0]

# === Extract bead numbers at interface ===
beads_at_interface = np.zeros((Length_LC, len(interface_clusters)), dtype=int)
for idx, cid in enumerate(interface_clusters):
    beads_at_interface[:, idx] = LC[:, cid - 1]  # Convert to 0-based indexing

# === Separate polymers interface beads ===
m_pe = []
m_p3hb = []
for m in range(beads_at_interface.shape[1]):
    for k in range(beads_at_interface.shape[0]):
        bead_id = beads_at_interface[k, m]
        if bead_id != 0:
            matches = np.where(all_bead_no == bead_id)[0]
            for i in matches:
                if str(atoms[i, 3]).strip() == 'PET':
                    m_pe.append(bead_id)
                elif str(atoms[i, 3]).strip() == 'PLA':
                    m_p3hb.append(bead_id)

# === Compute ratios ===
total = len(m_pe) + len(m_p3hb)
ratio_pe = len(m_pe) / total * 100 if total > 0 else 0
ratio_p3hb = len(m_p3hb) / total * 100 if total > 0 else 0

print(f"ratio_pe = {ratio_pe:.2f}%")
print(f"ratio_p3hb = {ratio_p3hb:.2f}%")

# === Save to Excel ===
output_path = 'analysis.xlsx'
df_out = pd.DataFrame([[ratio_p3hb, ratio_pe]])
with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    df_out.to_excel(writer, sheet_name='P3HB_PE together', index=False, header=False, startrow=0, startcol=0)

# === Call next Python script ===
os.system('python add_0_p3hbbulk.py')


##############################################################
import pandas as pd

# Load the entire Excel file (all sheets)
with pd.ExcelWriter('analysis.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    # Read the specific sheet
    df = pd.read_excel('analysis.xlsx', sheet_name='interface_and_pe', header=None)

    # Step 1: Swap column 2 (index 1) and column 3 (index 2)
    df.iloc[:, [1, 2]] = df.iloc[:, [2, 1]].values

    # Step 2: Move rows with 0 in column 2 (index 1) to the end
    non_zero_rows = df[df.iloc[:, 1] != 0]
    zero_rows = df[df.iloc[:, 1] == 0]
    reordered_df = pd.concat([non_zero_rows, zero_rows], ignore_index=True)

    # Write it back to the same sheet, replacing the content
    reordered_df.to_excel(writer, sheet_name='interface_and_pe', index=False, header=False)

##########################################



print(f"Elapsed time: {time.time() - start_time:.2f} seconds")