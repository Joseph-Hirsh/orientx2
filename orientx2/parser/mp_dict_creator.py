import csv
import json

# Initialize an empty dictionary to hold the mapping
twitter_dict = {}

# Open and read the CSV file
with open('/assets/uk_c&l_mps.csv', mode='r') as file:
    reader = csv.DictReader(file)

    # Iterate through each row in the CSV
    for row in reader:
        # Extract the Twitter handle
        twitter_handle = row['Twitter']

        # Skip rows with Twitter handle 'NONE'
        if twitter_handle == 'NONE':
            continue

        # Extract the rest of the information
        name_party_referendum = {
            'Name': row['Name'],
            'Party': row['Party'],
            'Referendum vote': row['Referendum vote']
        }

        # Add to the dictionary
        twitter_dict[twitter_handle] = name_party_referendum

# Write the dictionary to a JSON file
with open('/Users/josephhirsh/Documents/GitHub/orientx2/assets/uk_mps.json', 'w') as json_file:
    json.dump(twitter_dict, json_file, indent=4)

# Confirm the write process
print("Dictionary has been written to uk_mps.json")
