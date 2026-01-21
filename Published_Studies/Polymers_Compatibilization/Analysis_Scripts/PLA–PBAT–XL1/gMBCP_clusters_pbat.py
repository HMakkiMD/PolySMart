import pandas as pd
import glob

# Automatically find the file that starts with 'network' and ends with '.xlsx'
file_list = glob.glob("network*.xlsx")

if not file_list:
    raise FileNotFoundError("No file starting with 'network' found in this folder.")

file_name = file_list[0]  # use the first match

print(f"Detected file: {file_name}")

# Sheet name
sheet_name = "histogram-matrix"

df = pd.read_excel(file_name, sheet_name=sheet_name)

# Define the two bead ranges
range1_min, range1_max = 1, 121680 # for PLA
range2_min, range2_max = 125281, 262170 # for PBAT

# List to store selected columns
selected_columns = []

# Loop through each column
for column in df.columns:
    col_data = df[column].dropna()  # remove NaN values
    
    has_range1 = col_data.between(range1_min, range1_max).any()
    has_range2 = col_data.between(range2_min, range2_max).any()

    # If both conditions are true, save the column name
    if has_range1 and has_range2:
        selected_columns.append(column)

# Filter dataframe to the selected columns
filtered_df = df[selected_columns]

# Save to new Excel file
output_file = "gmbcp_clusters.xlsx"
filtered_df.to_excel(output_file, index=False)

print(f"Done! {len(selected_columns)} column(s) saved to {output_file}.")
