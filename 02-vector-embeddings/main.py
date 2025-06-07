from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI()

# System prompt: sets the persona
system_prompt = {
    "role": "system",
    "content": (
        "You are a friendly German teacher helping students who are learning German at an institute. "
        "You explain grammar, vocabulary, and pronunciation in the simplest way possible. "
        "Avoid complex terms and use simple examples. If students seem confused, break it down more. "
        "Always encourage them kindly and make learning fun."
    )
}

# User prompt: question from the student
user_prompt = {
    "role": "user",
    "content": "Can you explain the difference between 'der', 'die', and 'das'?"
}

# Send request to OpenAI
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[system_prompt, user_prompt]
)

# Print response
print(response.choices[0].message.content)
