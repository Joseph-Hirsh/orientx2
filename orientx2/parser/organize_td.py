import csv

# Function to read the CSV, sort the rows, and write the output to a new CSV
def sort_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip header row

        # Separate rows based on label
        input_rows = []
        output_rows = []
        both_rows = []
        neither_rows = []
        no_label_rows = []

        # Iterate over rows and classify them
        for row in reader:
            label = row[0].strip() if row else ''
            if label == 'Input':
                input_rows.append(row)
            elif label == 'Output':
                output_rows.append(row)
            elif label == 'Both':
                both_rows.append(row)
            elif label == 'Niether':
                neither_rows.append(row)
            elif not label:  # No label (empty label column)
                no_label_rows.append(row)
            else:
                neither_rows.append(row)  # For unexpected labels, put them under 'Neither'

        # Write the sorted rows to the output file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Write header first
            writer.writerows(input_rows)  # Write 'Input' rows
            writer.writerows(output_rows)  # Write 'Output' rows
            writer.writerows(both_rows)  # Write 'Both' rows
            writer.writerows(neither_rows)  # Write 'Niether' rows
            writer.writerows(no_label_rows)  # Write rows with no label

# Specify the input and output file paths
input_csv = '/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv'  # Path to your input CSV
output_csv = '/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv'  # Path to your output CSV

# Call the function to sort the CSV
sort_csv(input_csv, output_csv)

print("CSV has been sorted and saved to", output_csv)
