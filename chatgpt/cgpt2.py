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
  #answers = []

  # get the first response

  time0 = timeit.default_timer()
  # loop to get multiple responses
  for i in range(2):
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
    answers = [response['choices'][0]['message']['content']]
    #answers = []
    
    # append the answer to the list
    #answers.append(answer)
    write_to_json(answers, "testdata.json")
    """
    # ask the user if they want to continue
    user_input = input("Do you want another response? (y/n): ")
    
    # break the loop if the user says no
    if user_input.lower() != 'y':
        break
    """
    
  return answers

def write_to_json(list, filename):
    remove_last_line(filename)
    with open(filename, "a") as outfile:
        outfile.write(",")
        outfile.write("\n")
        for json_object in list:
            outfile.write(str(json_object))
            if json_object != list[-1]:
                outfile.write(",")
            outfile.write("\n")
        outfile.write("]")
    return outfile

def remove_last_line(filename):                     # Från https://stackoverflow.com/questions/1877999/delete-final-line-in-file-with-python
    with open(filename, "r+", encoding = "utf-8") as file:

        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()


# Writing to sample.json
def write_to_json_old(list):
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
    main()
    #answers = main()
    #print_answers(answers)
    #write_to_json(answers, "testdata.json")