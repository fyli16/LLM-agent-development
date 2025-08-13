from openai import OpenAI
client = OpenAI()

def call_openai():

    result = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": "Write an poem of python."},
        ],
        # max_completion_tokens=256, 
        # temperature=1,
        stream=True,
    )

    for chunk in result:
        print(chunk.choices[0].delta.content, flush=True, end="")
    print('\n')

call_openai()