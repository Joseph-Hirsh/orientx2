import csv
import json
import re

# Function to standardize and compare names
def standardize_name(name):
    # Convert "Doe, John" to "John Doe"
    if ',' in name:
        last_name, first_name = map(str.strip, name.split(',', 1))
        name = f"{first_name} {last_name}"
    # Remove text in parentheses
    name = re.sub(r'\s*\(.*?\)\s*', ' ', name).strip()
    return name

def replace_none_with_handles(csv_file, json_file, output_csv):
    # Load JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Create a name to Twitter handle mapping from the JSON data
    name_to_twitter = {}
    for tweet in json_data:
        # Standardize the name
        name = standardize_name(tweet['user']['name'])
        twitter_handle = tweet['user']['screen_name']
        name_to_twitter[name] = twitter_handle

    # Load the CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        csv_data = list(csv.DictReader(f))

    # Update the CSV data
    for row in csv_data:
        if row['Twitter'] == "NONE":
            # Standardize the name and find the corresponding Twitter handle
            standardized_name = standardize_name(row['Name'])
            twitter_handle = name_to_twitter.get(standardized_name, "NONE")
            row['Twitter'] = twitter_handle

    # Write the updated data to the output CSV file
    with open(output_csv, 'w', encoding='utf-8', newline='') as out_file:
        fieldnames = ["Name", "Party", "Twitter", "Referendum vote"]
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Updated CSV has been created: {output_csv}")

# Example usage:
replace_none_with_handles('/assets/uk_c&l_mps.csv',
                          '/Users/josephhirsh/Documents/GitHub/orientx2/assets/MPs.tweets.json',
                          '/Users/josephhirsh/Documents/GitHub/orientx2/assets/output2.csv')
