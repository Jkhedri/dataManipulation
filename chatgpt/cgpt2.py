import openai
import os
from dotenv import load_dotenv
import timeit
import math

# Okej man måste kalla på load_dotenv() när man vill använda .env filen
load_dotenv()
ITERATIONS = 100  # number of iterations

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

  time0 = timeit.default_timer()
  # loop to get multiple responses
  for i in range(ITERATIONS):
    starttime = timeit.default_timer()
    # get a single response from the API
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [
      {"role": "system", "content":instruction_prompt},
      {"role": "user", "content":"Please come up with 2 prompts and answers, "\
       "and return the data in the format described previously and nothing else. "\
         "Both the prompts and answers shall be anywhere in the range of 10 to 100 words, no less, no more. "\
          "Separate the different pairs of prompt-and-answers with a comma (,). "\
            "Remember to include the brackets and surround the prompt and answers with citations. "\
              "Also remember to indent them."},],
    n=1,
    stop=None,
    temperature=math.log(1.65+0.0106*i), #(temp will range from 0.5 to 1)
    )
    print("- Iteration:", i+1)
    print("- Time for iteration:", round(timeit.default_timer() - starttime), "seconds")
    print("- Total runtime:", round(timeit.default_timer() - time0), "seconds", "\n")

    # get the answer from the response
    answer = response['choices'][0]['message']['content']
    
    # append the answer to the list
    answers.append(answer)
    """
    # ask the user if they want to continue
    user_input = input("Do you want another response? (y/n): ")
    
    # break the loop if the user says no
    if user_input.lower() != 'y':
        break
    """
    
  return answers

# Writing to sample.json
def write_to_json(list):
    with open("pnatemp0p5n6.json", "w") as outfile:
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
    answers = main()
    #print_answers(answers)
    write_to_json(answers)