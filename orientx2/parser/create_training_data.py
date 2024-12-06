import pandas as pd

# Load the original CSV
input_csv = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/parsed_posts.csv"  # Replace with your file name
output_csv = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/td_working.csv"

# Read the input CSV
data = pd.read_csv(input_csv)

# Define subsets
conditions = [
    {"party": "Conservative", "referendum vote": "Remain"},
    {"party": "Conservative", "referendum vote": "Leave"},
    {"party": "Labour", "referendum vote": "Remain"},
    {"party": "Labour", "referendum vote": "Leave"},
]

# Create an empty DataFrame for the training dataset
training_data = pd.DataFrame(columns=["label", "text"])

# Process each subset
for condition in conditions:
    subset = data[
        (data["party"] == condition["party"]) &
        (data["referendum vote"] == condition["referendum vote"])
        ]

    # Randomly sample 100 rows
    sampled_subset = subset.sample(n=200, random_state=2)  # Adjust `random_state` for reproducibility

    # Add to the training dataset with blank labels
    training_data = pd.concat(
        [
            training_data,
            pd.DataFrame({"label": "", "text": sampled_subset["content"]})
        ],
        ignore_index=True
    )

# Save the training dataset to a new CSV
training_data.to_csv(output_csv, index=False)

print(f"Training dataset saved to {output_csv}")
