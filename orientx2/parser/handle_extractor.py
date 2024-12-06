import re

# Define a function to extract Twitter handles from a JSON file
def extract_handles_from_json(json_file_path):
    handle_pattern = r"@\w+"  # Regex pattern for Twitter handles

    with open(json_file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # Read the entire file as a string

    handles = set(re.findall(handle_pattern, content))  # Find all handles and store unique ones
    return handles

# Provide the JSON file path
json_file_path = '/Users/josephhirsh/Documents/GitHub/orientx2/assets/MPs.tweets.json'
twitter_handles = extract_handles_from_json(json_file_path)

# Print or save the extracted handles
print(f"Extracted {len(twitter_handles)} Twitter handles:")
for handle in twitter_handles:
    print(handle)
