import ollama
import os
import re
import json

# Parameters for the model
model_name = "llama3:8b-instruct-q8_0"

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

# Directories
prompts_dir = "Prompts"
output_dir = "Prompt-Replies"
os.makedirs(output_dir, exist_ok=True)

# Function to append a response to the JSON file
def append_response_to_file(file_path, number, prompt_text, reply):
    data = {
        'number': number,
        'prompt': prompt_text,
        'response': reply
    }
    
    if os.path.exists(file_path):
        with open(file_path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=2)
    else:
        with open(file_path, 'w') as file:
            json.dump([data], file, indent=2)

# Function to find the highest processed number in a given JSON file
def find_highest_processed_number(file_path):
    if not os.path.exists(file_path):
        return 0
    
    with open(file_path, 'r') as file:
        file_data = json.load(file)
        if not file_data:
            return 0
        return max(item['number'] for item in file_data)

# Function to find the highest numbered JSON file and the highest processed prompt number within it
def find_resume_point(output_dir):
    json_files = sorted([f for f in os.listdir(output_dir) if f.startswith("prompt-replies-") and f.endswith(".json")], key=lambda x: int(re.findall(r'\d+', x)[0]))
    if not json_files:
        return None, 0
    
    highest_json_file = json_files[-1]
    highest_json_path = os.path.join(output_dir, highest_json_file)
    highest_number = find_highest_processed_number(highest_json_path)
    
    return highest_json_file, highest_number

# Function to process each prompt and generate a response
def process_prompt_file(file_path, output_file_path, start_number=1):
    # Read the prompts from the file
    with open(file_path, 'r') as file:
        prompts = file.readlines()
    
    for i, prompt in enumerate(prompts, start=1):
        # Skip already processed prompts
        if i < start_number:
            continue

        # Remove the numbered list part (e.g., "1. ", "2. ", etc.)
        prompt_text = re.sub(r'^\d+\.\s*', '', prompt).strip()
        
        messages = [
            {
                'role': 'user',
                'content': prompt_text,
            },
            {
                'role': 'assistant',
                'content': 'Sure:\n1.'
            }
        ]

        # Get the response from the model
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options=options,
            stream=False,
        )

        reply = response['message']['content']

        # Append the response to the JSON file
        append_response_to_file(output_file_path, i, prompt_text, reply)

# Find the highest numbered JSON file and the highest processed prompt number within it
highest_json_file, highest_number = find_resume_point(output_dir)

# Determine starting point for processing
if highest_json_file:
    highest_json_num = int(re.findall(r'\d+', highest_json_file)[0])
    if highest_number < 100:
        start_prompt_file = f"prompt-{highest_json_num}.txt"
        start_number = highest_number + 1
    else:
        start_prompt_file = f"prompt-{highest_json_num + 100}.txt"
        start_number = 1
else:
    start_prompt_file = "prompt-100.txt"
    start_number = 1

# Print the resume information
print(f"Highest JSON file: {highest_json_file}")
print(f"Highest prompt number in the highest JSON file: {highest_number}")
print(f"Starting from prompt file: {start_prompt_file} and prompt number: {start_number}")

# Process all prompt files in order starting from the correct point
prompt_files = sorted([f for f in os.listdir(prompts_dir) if f.startswith("prompt-") and f.endswith(".txt")], key=lambda x: int(re.findall(r'\d+', x)[0]))

for prompt_file in prompt_files:
    if prompt_file < start_prompt_file:
        continue
    
    file_path = os.path.join(prompts_dir, prompt_file)
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(prompt_file)[0].replace('prompt-', 'prompt-replies-')}.json")
    
    if prompt_file == start_prompt_file:
        start_num = start_number
    else:
        start_num = 1
    
    process_prompt_file(file_path, output_file_path, start_num)
