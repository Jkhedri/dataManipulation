# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.api_key = "key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": 'I want you to simulate snippets of psychology sessions.'\
          ' I want you to come up with a prompt from a patient and a response from a licensed psychologist to that prompt.'\
            ' I want you to return to me the data in JSON format as follows:\n'\
              '{\n'\
                '"prompt": YOUR PROMPT\n'\
                  '"answer": YOUR ANSWER\n'\
                    '}\n'\
                      'Please return only the data in the described format and nothing more. Remember to include the brackets and surround the prompt and answer with citations. Understood?'},
        {"role": "user", "content": "Please come up with a prompt and answer and return the data in JSON format as described."},
    ],
)

print(response['choices'][0]['message']['content'])