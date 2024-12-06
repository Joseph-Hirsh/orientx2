import pandas as pd
import random


# Load the CSV
def add_orientation_column(csv_file, output_file):
    """
    Adds a column called 'orientation' to the CSV, with random values from 0 to 3.

    Parameters:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to save the output CSV file.
    """
    # Load the CSV into a DataFrame
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
        return
    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}")
        return

    # Add the 'orientation' column with random values from 0 to 3
    df['orientation'] = [random.randint(0, 3) for _ in range(len(df))]

    # Save the modified DataFrame to a new CSV
    try:
        df.to_csv(output_file, index=False)
        print(f"Updated CSV saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving the CSV: {e}")


# Example usage
input_csv = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/parsed_posts.csv"  # Replace with the path to your input CSV
output_csv = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/classified_posts_for_stats.csv"  # Replace with your desired output file path
add_orientation_column(input_csv, output_csv)
