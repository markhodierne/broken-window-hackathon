import json

# Function to read JSON file into a dictionary
def read_json_to_dict(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

# Example usage
json_file_path = 'uploads/metadata.json'  # Replace with your JSON file path
data = read_json_to_dict(json_file_path)

def filter_comments_by_classification(data, classification):
    # Filter the dictionary to get comments based on classification
    filtered_comments = [entry['comment'] for entry in data if entry['classification'] == classification]
    return filtered_comments

# Filter comments with classification 'graffiti'
comments = filter_comments_by_classification(data, 'graffiti')
print("GRAFFITI SUMMARY:\n", comments)

# Filter comments with classification 'graffiti'
comments = filter_comments_by_classification(data, 'windows')
print("WINDOWS SUMMARY:\n", comments)