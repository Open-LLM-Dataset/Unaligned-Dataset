import os
import re
import json
import ollama

# Parameters for the model
model_name = "llama3:8b-instruct-q6_K"

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
prompts_dir = "Neutral-Prompts"
output_dir = "Neutral-Prompt-Replies"
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

# Function to process each prompt and generate a response
def process_prompt_file(file_path, output_file_path, start_number):
    # Read the prompts from the file
    with open(file_path, 'r') as file:
        prompts = file.readlines()[start_number - 1:]  # Adjusted to start from the specified number
    
    for i, prompt in enumerate(prompts, start=start_number):
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

# Load file and number values from the resume.json
with open('resume.json', 'r') as resume_file:
    resume_data = json.load(resume_file)
    file = resume_data.get('file', 100)
    number = resume_data.get('number', 1)

# Process all prompt files in order
prompt_files = sorted([f for f in os.listdir(prompts_dir) if f.startswith("prompt-") and f.endswith(".txt")], key=lambda x: int(x.split('-')[1].split('.')[0]))

for prompt_file in prompt_files:
    file_number = int(prompt_file.split('-')[1].split('.')[0])
    if file_number < file:
        continue
    file_path = os.path.join(prompts_dir, prompt_file)
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(prompt_file)[0].replace('prompt-', 'prompt-replies-')}.json")
    process_prompt_file(file_path, output_file_path, number)

    # Reset number to 1 for subsequent files
    number = 1

    print(f"Completed processing for {prompt_file}")
