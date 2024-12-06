import pandas as pd
import re


def remove_links(text):
    """
    Remove all links from the given text.

    Args:
        text (str): The text to clean.

    Returns:
        str: The text with all links removed.
    """
    if isinstance(text, str):
        return re.sub(r'http[s]?://\S+', '', text).strip()
    return text


def clean_csv(input_csv, output_csv):
    """
    Load a CSV file, remove links from the 'text' column, and save the cleaned data to a new CSV file.

    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to save the cleaned CSV file.
    """
    try:
        # Load the dataset with proper quoting and error handling
        df = pd.read_csv(input_csv, quotechar='"', on_bad_lines='skip', encoding='utf-8')

        if 'text' not in df.columns:
            raise ValueError("Input CSV does not contain a 'text' column.")

        # Remove links from the 'text' column
        df['text'] = df['text'].apply(remove_links)

        # Save the cleaned data
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Cleaned dataset saved to '{output_csv}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # File paths
    input_csv = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv"  # Replace with the path to your input CSV file
    output_csv = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working2.csv"  # Replace with the desired output path

    # Clean the CSV
    clean_csv(input_csv, output_csv)
