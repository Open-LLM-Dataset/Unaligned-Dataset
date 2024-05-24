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
def append_response_to_file(file_path, prompt_text, reply):
    data = {
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
def process_prompt_file(file_path, output_file_path, start_index=0):
    # Read the prompts from the file
    with open(file_path, 'r') as file:
        prompts = file.readlines()[start_index:]

    for i, prompt in enumerate(prompts, start=start_index+1):
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
        append_response_to_file(output_file_path, prompt_text, reply)

        print(f"Processed and appended response for prompt: {prompt_text}")

        # Update the progress index
        with open("progress.json", "w") as progress_file:
            json.dump({"file_path": file_path, "index": i}, progress_file)

# Check if there is a progress file to resume from
if os.path.exists("progress.json"):
    with open("progress.json", "r") as progress_file:
        progress_data = json.load(progress_file)
        prompt_file = progress_data["file_path"]
        start_index = progress_data["index"]
        print(f"Resuming processing from file: {prompt_file}, index: {start_index}")
        process_prompt_file(prompt_file, os.path.join(output_dir, f"{os.path.splitext(os.path.basename(prompt_file))[0].replace('prompt-', 'prompt-replies-')}.json"), start_index=start_index)
        print("Processing resumed successfully.")
else:
    # Process all prompt files in order
    prompt_files = sorted([f for f in os.listdir(prompts_dir) if f.startswith("prompt-") and f.endswith(".txt")])

    for prompt_file in prompt_files:
        file_path = os.path.join(prompts_dir, prompt_file)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(prompt_file)[0].replace('prompt-', 'prompt-replies-')}.json")
        process_prompt_file(file_path, output_file_path)

        print(f"Completed processing for {prompt_file}")
