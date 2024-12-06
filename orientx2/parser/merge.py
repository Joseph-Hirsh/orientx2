import csv
from fuzzywuzzy import fuzz, process

import csv
import re
from fuzzywuzzy import fuzz, process


import csv
import re
from fuzzywuzzy import fuzz, process


def create_combined_csv(first_csv, second_csv, output_csv):
    # Function to standardize names
    def standardize_name(name):
        # Convert "Doe, John" to "John Doe"
        if ',' in name:
            last_name, first_name = map(str.strip, name.split(',', 1))
            name = f"{first_name} {last_name}"
        # Remove text in parentheses
        name = re.sub(r'\s*\(.*?\)\s*', ' ', name).strip()
        # Replace nicknames
        name_parts = name.split()
        name_parts = [
            part if part not in nickname_map else nickname_map[part]
            for part in name_parts
        ]
        return ' '.join(name_parts)

    # Nickname mapping
    nickname_map = {
        "Bill": "William",
        "Bob": "Robert",
        "Nick": "Nicholas"
    }

    # Load the first CSV into a list of dictionaries
    with open(first_csv, 'r', encoding='utf-8') as f1:
        first_data = list(csv.DictReader(f1))

    # Load the second CSV into a list of dictionaries
    with open(second_csv, 'r', encoding='utf-8') as f2:
        second_data = list(csv.DictReader(f2))

    # Prepare the output data
    combined_data = []

    for person in first_data:
        # Standardize name from first CSV
        full_name_1 = standardize_name(person['Name'])

        # Search for the best match in the second CSV
        names_in_second_csv = [standardize_name(entry['Name']) for entry in second_data]
        best_match, score = process.extractOne(full_name_1, names_in_second_csv, scorer=fuzz.token_sort_ratio)

        # If the match score is high enough, get the Twitter handle
        if score > 80:  # Adjust the threshold as needed
            matched_entry = next(entry for entry in second_data if standardize_name(entry['Name']) == best_match)
            twitter_handle = matched_entry['Twitter'].strip() if matched_entry['Twitter'].strip() else "NONE"
        else:
            twitter_handle = "NONE"

        # Collect the combined data
        combined_data.append({
            "Name": full_name_1,
            "Party": person['Party'],
            "Referendum vote": person['Referendum vote'],
            "Twitter": twitter_handle
        })

    # Sort data: Rows with NONE in the Twitter field at the top
    combined_data.sort(key=lambda x: x['Twitter'] == "NONE", reverse=True)

    # Write the combined data to the output CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=["Name", "Party", "Twitter", "Referendum vote"])
        writer.writeheader()
        writer.writerows(combined_data)

    print(f"Combined CSV has been created: {output_csv}")



create_combined_csv('/Users/josephhirsh/Documents/GitHub/orientx2/assets/brexit_positions.csv',
                    '/Users/josephhirsh/Documents/GitHub/orientx2/assets/uk_mps.csv',
                    '/Users/josephhirsh/Documents/GitHub/orientx2/assets/uk_c&l_mps.csv')
