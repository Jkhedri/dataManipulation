import openai
import os


def main():
  openai.api_key = os.getenv("OPENAI_API_KEY")

  # define the long instruction prompt
  instruction_prompt = 'I want you to simulate snippets of psychology sessions.'\
            ' I want you to come up with a prompt from a patient and then two responses to that prompt: One response from a licensed psychologist (a good response), and one response that is considered a bad, unethical, uneducated response'\
            ' If I ask you to return multiple prompts, I want every prompt to be on a different subject than the previous one.'\
              ' I want you to return the data to me in the following format:\n'\
                '{\n'\
                  '   "prompt": YOUR PROMPT\n'\
                    '   "g_answer": YOUR GOOD ANSWER\n'\
                      '   "b_answer": YOUR BAD ANSWER\n'\
                        '}\n'\
                          'Please return only the data in the described format and nothing more. Understood?'

  # initialize the answers list
  answers = []

  # get the first response


  # loop to get multiple responses
  while True:
      # get a single response from the API
      response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages = [
        {"role": "system", "content":instruction_prompt},
        {"role": "user", "content":"Please come up with five prompts and answers, and return the data in the format described previously and nothing else. Separate the different pairs of prompt-and-answers with a comma (,). Remember to include the brackets and surround the prompt and answers with citations. Also remember to indent them."},],
      max_tokens=2048,
      n=1,
      stop=None,
      temperature=0.7,
      )
      
      # get the answer from the response
      answer = response['choices'][0]['message']['content']
      
      # append the answer to the list
      answers.append(answer)
      
      # ask the user if they want to continue
      user_input = input("Do you want another response? (y/n): ")
      
      # break the loop if the user says no
      if user_input.lower() != 'y':
          break

  return answers

# Writing to sample.json
def write_to_json(list):
    with open("pna5.json", "w") as outfile:
        outfile.write("[")
        outfile.write("\n")
        for json_object in list:
            outfile.write(json_object)
            if json_object != list[-1]:
                outfile.write(",")
            outfile.write("\n")
        outfile.write("]")
    return outfile

def print_answers(answers):
    for answer in answers:
        print(answer)

if __name__ == "__main__":
    #answers = main()
    #print_answers(answers)
    #write_to_json(answers)
    print(os.getenv("OPENAI_API_KEY"))