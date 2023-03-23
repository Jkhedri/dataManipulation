import random
import os
import sys


num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for i in range(len(num_list)):
    num_list[i] = random.randint(1, 100) * num_list[i]
    



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
        if pos-1 > 0:
            file.seek(pos-1, os.SEEK_SET)
            file.truncate()



if __name__ == "__main__":
    print(num_list)
    file = write_to_json(num_list, "beans.json")
    print(file)