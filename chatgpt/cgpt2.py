import openai

openai.api_key = "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"

# define the long instruction prompt
instruction_prompt = 'I want you to simulate snippets of psychology sessions.'\
          ' I want you to come up with a prompt from a patient and a response from a licensed psychologist to that prompt.'\
            ' I want you to return to me the data in JSON format as follows:\n'\
              '{\n'\
                '"prompt": YOUR PROMPT\n'\
                  '"answer": YOUR ANSWER\n'\
                    '}\n'\
                      'Please return only the data in the described format and nothing more. Remember to include the brackets and surround the prompt and answer with citations. Understood?'

# initialize the answers list
answers = []

# get the first response
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    prompt=instruction_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

# loop to get multiple responses
while True:
    # get a single response from the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        prompt="Generate one more pair, please.",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    # get the answer from the response
    answer = response.choices[0].text.strip()
    
    # append the answer to the list
    answers.append(answer)
    
    # ask the user if they want to continue
    user_input = input("Do you want another response? (y/n): ")
    
    # break the loop if the user says no
    if user_input.lower() != 'y':
        break

# print the answers
for answer in answers:
    print(answer)