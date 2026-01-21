import pandas as pd

# Define a function to count row occurrences in a text file and write to Excel
def count_row_occurrences_to_excel(file_name, output_file):
    row_counts = {}  # Dictionary to store row counts

    with open(file_name, 'r') as file:
        for line in file:
            row = line.strip()  # Remove leading/trailing whitespace
            if row in row_counts:
                row_counts[row] += 1
            else:
                row_counts[row] = 1

    # Convert row_counts dictionary to a list of dictionaries for DataFrame
    data = []
    for row, count in row_counts.items():
        elements = row.split()  # Split the row into elements
        row_data = {'Count': count}
        for i, element in enumerate(elements):
            row_data[f'Element_{i + 1}'] = int(float(element))  # Convert element to integer
        data.append(row_data)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Write the DataFrame to an existing Excel file with a new sheet name
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name='interface_and_pe', index=False, header=False)

# Specify the file names
input_file = 'interface_and_pe.txt'
output_file = 'analysis.xlsx'  # Use the existing Excel file

# Call the function to count row occurrences and write to Excel
count_row_occurrences_to_excel(input_file, output_file)

print(f"Data has been written to the 'interface_and_pe' sheet in '{output_file}'.")
