import os
import pandas as pd
import openpyxl

def parse_itp_file(itp_file_path):
    data = {}
    section_name = None

    with open(itp_file_path, 'r') as itp_file:
        for line in itp_file:
            line = line.strip()

            if line.startswith(';') or not line:
                # Skip comments and empty lines
                continue

            if line.startswith('[') and line.endswith(']'):
                # Start of a new section
                section_name = line[1:-1]
                data[section_name] = []
            else:
                if section_name:
                    # Append data to the current section
                    data[section_name].append(line.split())

    return data

def itp_to_excel(input_folder, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        itp_files = [file for file in os.listdir(input_folder) if file.endswith('.itp')]

        for itp_file in itp_files:
            itp_file_path = os.path.join(input_folder, itp_file)
            output_excel_file = os.path.splitext(itp_file)[0] + '.xlsx'
            output_excel_file_path = os.path.join(output_folder, output_excel_file)

            # Parse .itp file and extract data
            itp_data = parse_itp_file(itp_file_path)

            # Write data to Excel file
            with pd.ExcelWriter(output_excel_file_path, engine='openpyxl') as writer:
                for section, section_data in itp_data.items():
                    if section == ' atoms ':
                        df = pd.DataFrame(section_data)
                        df.to_excel(writer, sheet_name=section, index=False, header=False)
                    elif section in [' bonds ', ' constraints ']:
                        df = pd.DataFrame(section_data)
                        df = df.iloc[:, :2]  # Include only the first two columns
                        if 'Bonds_Constraints' in writer.sheets:
                            start_row = writer.sheets['Bonds_Constraints'].max_row + 1
                        else:
                            start_row = 0
                        
                        # Check if it's the 'constraints' section, and skip an empty row
                        if section == ' constraints ':
                            start_row -= 1
                        
                        df.to_excel(writer, sheet_name='Bonds_Constraints', index=False, header=False, startrow=start_row)

            print(f"Conversion successful. Data from {itp_file} written to {output_excel_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example:
if __name__ == "__main__":
    input_folder = "E:\loop"  # Replace with the path to your folder containing .itp files
    output_folder = "E:\loop" # Replace with the path to your desired output folder for Excel files
    itp_to_excel(input_folder, output_folder)
