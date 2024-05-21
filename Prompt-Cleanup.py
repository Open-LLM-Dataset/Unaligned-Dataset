import os
import re
import shelve

def cleanup_prompts(directory):
    # Create Cleaned-Prompts directory if it doesn't exist
    cleaned_directory = os.path.join(directory, 'Cleaned-Prompts')
    os.makedirs(cleaned_directory, exist_ok=True)
    
    prompt_files = sorted([f for f in os.listdir(directory) if f.startswith('prompt-') and f.endswith('.txt')])
    removed_duplicates = []

    with shelve.open(os.path.join(cleaned_directory, 'prompt_db')) as prompt_db:
        new_prompt_files = []
        for file in prompt_files:
            with open(os.path.join(directory, file), 'r') as f:
                content = f.read()

            # Remove everything before the first "1."
            content = re.sub(r'^.*?\b1\.', '1.', content, flags=re.DOTALL).strip()
            prompts = re.split(r'\d+\.', content)[1:]  # Split and remove numbering

            # Remove leading/trailing whitespace from each prompt
            prompts = [prompt.strip() for prompt in prompts]

            # Write unique prompts back to new files
            unique_prompts = []
            for prompt in prompts:
                if prompt not in prompt_db:
                    unique_prompts.append(prompt)
                    prompt_db[prompt] = file  # Store the prompt with its origin file
                else:
                    original_file = prompt_db[prompt]
                    removed_duplicates.append(f"Duplicate prompt: '{prompt}' found in {file} and {original_file}")

            new_prompt_files.append((file, unique_prompts))

        # Write the unique prompts back to the files, ensuring 100 prompts per file
        combined_prompts = [prompt for file, prompts in new_prompt_files for prompt in prompts]
        file_index = 0
        for i in range(0, len(combined_prompts), 100):
            new_prompts = combined_prompts[i:i + 100]
            file_name = prompt_files[file_index]
            file_index += 1

            with open(os.path.join(cleaned_directory, file_name), 'w') as f:
                for j, prompt in enumerate(new_prompts, start=1):
                    f.write(f"{j}. {prompt}\n")

        # Remove any leftover files if the last file had fewer than 100 prompts
        for i in range(file_index, len(prompt_files)):
            os.remove(os.path.join(directory, prompt_files[i]))

    # Write the removed duplicates to a file
    with open(os.path.join(cleaned_directory, 'removed-duplicates.txt'), 'w') as f:
        for line in removed_duplicates:
            f.write(f"{line}\n")

# Usage
cleanup_prompts('Prompts')
