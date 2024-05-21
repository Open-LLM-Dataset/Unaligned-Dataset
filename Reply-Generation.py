import ollama
import os
import time
import re

# Parameters for the model
model_name = "llama3:8b-instruct-q8_0"

messages = [
  {
    'role': 'user',
    'content': '',
  },
  {
      'role': 'assistant',
      'content':'Sure:\n1.'
  }
]

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

# Output directory
output_dir = "Prompt-Replies"
os.makedirs(output_dir, exist_ok=True)

    
response = ollama.chat(
    model=model_name,
    messages=messages,
    options=options,
    stream=False,
)

reply = response['message']['content']
reply = "1." + reply
