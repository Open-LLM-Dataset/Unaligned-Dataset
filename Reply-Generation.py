import ollama
import os
import json
import re

# Parameters for the model
model_name = "nous-hermes2:10.7b-solar-q6_K"

options = {
    "num_ctx": 2048,
    "repeat_last_n": 64,
    "repeat_penalty": 1.1,
    "temperature": 0.8,
    "tfs_z": 1,
    "top_k": 40,
    "top_p": 0.9,
    "num_predict": -1  # Generate until the model stops
}

prompts_dir = "Prompts"
response_dir = "Prompt-Response"

if not os.path.exists(response_dir):
    os.makedirs(response_dir)

# Function to extract the number from the filename
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

# Find the highest numbered JSON file
existing_json_files = [f for f in os.listdir(response_dir) if f.startswith("prompt-") and f.endswith(".json")]
existing_json_files.sort(key=lambda f: extract_number(f), reverse=True)

# Start from the highest existing JSON file or from scratch if none exist
start_from_file = extract_number(existing_json_files[0]) if existing_json_files else None

# Process each text file in order, starting from the appropriate point
for filename in sorted(os.listdir(prompts_dir), key=lambda f: extract_number(f)):
    file_number = extract_number(filename)
    
    # Skip files that are lower than the starting point
    if start_from_file and file_number < start_from_file:
        continue

    file_path = os.path.join(prompts_dir, filename)
    response_path = os.path.join(response_dir, filename.replace(".txt", ".json"))

    if os.path.exists(response_path) and file_number == start_from_file:
        with open(response_path, 'r') as response_file:
            responses = json.load(response_file)
    else:
        responses = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Remove the number at the beginning of the line
            instruction = ' '.join(line.split(' ')[1:]).strip()

            # Generate the response from the model
            response = ollama.generate(
                model=model_name,
                prompt=instruction,
                options=options,
                stream=False
            )

            reply = response['response']

            # Append the original instruction and the response to the list
            responses.append({"instruction": instruction, "response": reply})

            # Save the responses to the JSON file
            with open(response_path, 'w') as response_file:
                json.dump(responses, response_file, indent=4)

print("All prompts have been processed and responses saved.")
