import os

import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)

client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
MODEL_NAME = "DeepSeek-R1"

# Not supported: temperature, top_p, tools
# max_tokens is supported BUT that may end up cutting off a thought process!
# stop is also supported
completion = client.chat.completions.create(
    model=MODEL_NAME,
    n=1,
    messages=[
        {"role": "user", "content": "who painted the mona lisa?"},
    ],
    stream=True
)

print("Response: ")
is_thinking = False
for event in completion:
    if event.choices:
        content = event.choices[0].delta.content
        if content == "<think>":
            is_thinking = True
            print("🧠 Thinking...", end="", flush=True)
        elif content == "</think>":
            is_thinking = False
            print("🛑\n\n")
        elif content:
            print(content, end="", flush=True)
