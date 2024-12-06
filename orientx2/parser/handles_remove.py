import pandas as pd
import re


def remove_handles(text):
    """
    Remove "RT @twitterhandle:" and "@twitterhandle" from text.
    Args:
        text (str): The input text.
    Returns:
        str: Cleaned text with handles removed.
    """
    # Remove "RT @twitterhandle:" at the beginning
    text = re.sub(r'\bRT @\w+:\s*', '', text)
    # Remove all other "@twitterhandle"
    #text = re.sub(r'@\w+', '', text)
    # Strip extra spaces and return
    return text.strip()


def clean_dataset(input_csv, output_csv):
    """
    Clean a dataset by removing Twitter handles and save the cleaned dataset.
    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to save the cleaned CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_csv)

    # Ensure the dataset has the required columns
    if 'label' not in df.columns or 'text' not in df.columns:
        raise ValueError("Input CSV must contain 'label' and 'text' columns.")

    # Clean the text column
    df['text'] = df['text'].apply(remove_handles)

    # Save the cleaned dataset to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Cleaned dataset saved to '{output_csv}'")


if __name__ == "__main__":
    # Replace with your input and output file paths
    input_csv_path = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv"
    output_csv_path = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv"

    clean_dataset(input_csv_path, output_csv_path)
