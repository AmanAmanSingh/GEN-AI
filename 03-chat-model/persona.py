from dotenv import load_dotenv
import os
from openai import OpenAI
from prompt import PERSONA_SYSTEM_PROMPT
from prompt import DOST_PERSONA_PROMPT


load_dotenv()
client = OpenAI()

system_prompt = {
    "role": "system",
    "content": DOST_PERSONA_PROMPT
}

# user_prompt = {
#     "role": "user",
#     "content": "hello"
# }

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[system_prompt, 
            { "role": "user", "content": "kya kar "},
            { "role": "assistant", "content": "tu pagal hai"},

    ],
    stream=True,
)

# print(response.choices[0].message.content)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)