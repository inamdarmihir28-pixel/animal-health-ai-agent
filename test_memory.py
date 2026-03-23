from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def chat_with_memory(messages):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return resp.choices[0].message.content

conversation = [
    {"role": "system", "content": "You are a helpful tutor."},
    {"role": "user", "content": "My name is Alex."},
]

# round 1
assistant_reply = chat_with_memory(conversation)
print("Round 1:", assistant_reply)

# append assistant response
conversation.append({"role": "assistant", "content": assistant_reply})

# round 2
conversation.append({"role": "user", "content": "What is my name?"})
reply2 = chat_with_memory(conversation)
print("Round 2:", reply2)

conversation.append({"role": "assistant", "content": reply2})
conversation.append({"role": "user", "content": "What was my first statement?"})
reply3 = chat_with_memory(conversation)
print("Round 3:", reply3)