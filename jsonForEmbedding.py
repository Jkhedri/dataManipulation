import sqlite3
import random
import string
import json


"""
This script fetches data from a sqlite database and writes it to a json file.

Need to add ways to include feedback and other data.
"""


databaseName = 'database'              # Databasename in string format
dbConnection = sqlite3.connect(databaseName+'.db') # Establishes database connection
dbCursor = dbConnection.cursor()    # Creates a query cursor

def fetchInteractions():
    try:
        query = """SELECT * FROM interactions""";  # Fetches a list of all interactio in the database
        dbCursor.execute(query)
        interactions = dbCursor.fetchall()                            
        dbConnection.commit()
        return interactions
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def getPrompt(tuple):
    return tuple[0]

def getResponse(tuple):
    return tuple[5]

def getRandomString(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Data to be written

items = []
index = 1
for row in fetchInteractions():
    randomPromptString = getRandomString(10)
    randomResponseString = getRandomString(10)

    promptDictionary = {
        "id": index  ,
        "text": getPrompt(row)
        
    }

    index+=1
    responseDictionary = {
        "id": index,
        "text": getResponse(row)
        
    }
    index+=1

    # Serializing json
    json_prompt = json.dumps(promptDictionary, indent=4)
    json_response = json.dumps(responseDictionary, indent=4)
    items.append(json_prompt)
    items.append(json_response)

# Writing to sample.json
with open("for_embeddings.json", "w") as outfile:
    outfile.write("[")
    outfile.write("\n")
    for json_object in items:
        outfile.write(json_object)
        if json_object != items[-1]:
            outfile.write(",")
        outfile.write("\n")
    outfile.write("]")