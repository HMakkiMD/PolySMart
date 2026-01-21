import pandas as pd

# === File and Sheet Setup ===
filename = 'analysis.xlsx'
sheet_main = 'interface_and_pe'
sheet_extra = 'p3hb_bulk'

# === Load Data ===
df_main = pd.read_excel(filename, sheet_name=sheet_main, header=None)
df_extra = pd.read_excel(filename, sheet_name=sheet_extra, header=None)

# === Find the break point (where column 2 == 0) ===
zero_start_index = df_main[df_main.iloc[:, 1] == 0].index.min()

# === Prepare empty rows ===
empty_row = pd.DataFrame([[None]*df_main.shape[1]], columns=df_main.columns)

# === Build the new DataFrame ===
if pd.notna(zero_start_index):
    part_before = df_main.iloc[:zero_start_index]
    part_after = df_main.iloc[zero_start_index:]
    
    df_combined = pd.concat([
        part_before,
        empty_row,             # empty row before zeros
        part_after,
        empty_row,             # empty row after main data
        df_extra               # append p3hb_bulk data
    ], ignore_index=True)
else:
    # Fallback if no zero found: just append
    df_combined = pd.concat([
        df_main,
        empty_row,
        df_extra
    ], ignore_index=True)

# === Save the result back to the same sheet ===
with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_combined.to_excel(writer, sheet_name=sheet_main, index=False, header=False)
