import csv
import random


def create_balanced_dataset(filepath, output_filepath):
    # Load data from the CSV file
    label_0, label_1, label_2 = [], [], []

    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) < 2:
                continue
            label, text = row[0], row[1]
            if label == "Input":
                label_0.append((label, text))
            elif label == "Output":
                label_1.append((label, text))
            elif label == "Neither":
                label_2.append((label, text))

    # Ensure we don't exceed available tweets
    n_samples = min(len(label_1), len(label_2), len(label_0) // 2)

    # Randomly sample tweets from label 1 and label 2
    sampled_label_1 = random.sample(label_1, n_samples)
    sampled_label_2 = random.sample(label_2, n_samples)

    # Combine label 0 tweets with sampled tweets
    balanced_data = label_0 + [(1, text) for _, text in (sampled_label_1 + sampled_label_2)]

    # Write to the output CSV
    with open(output_filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["label", "text"])  # Header
        writer.writerows(balanced_data)

    print(f"Balanced dataset saved to {output_filepath}")


# Specify the input file and output file paths
input_filepath = '/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv'  # Replace with your actual input file name
output_filepath = '../../assets/td_0.csv'

# Create the balanced dataset
create_balanced_dataset(input_filepath, output_filepath)
