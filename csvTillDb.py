import sqlite3
import csv

# Initialisation
csvName = 'munwhu2022'               # Filename in string format. Should be matchname in format hhhaaayyyy
databaseName = 'tnlbc'              # Databasename in string format
dbConnection = sqlite3.connect(databaseName+'.db') # Establishes database connection
dbCursor = dbConnection.cursor()    # Creates a query cursor

# Read csv-file and save content to variable 'data'
with open(csvName+'.csv', 'r', encoding='utf-8') as f:  
    data = []           
    file = csv.reader(f, delimiter=';')
    header = next(file)
    for tuple in file:
        if len(tuple[5]) < 5:
            tuple[5] = '0' + tuple[5]
        elif len(tuple[5]) > 5:
            tuple[5] = tuple[5][0:5]
        tuple.append(csvName)
        if "Delete" in tuple[6]:        # Removes deleted tuples
            rowNumber = tuple[7].lstrip("Row: ")
            for row in data:
                if row[0] == rowNumber:
                    data.remove(row)
                    break
        else:
            data.append(tuple)
    f.close()

# Creates a table for the given csv-file in the given database-file
def createTable():
    matchName = csvName.upper()            #Matchname in format HHHAAAYYYY"
    headerString = "(Row, SeqID, Timestamp, LastModified, Period, MatchTime, EventType, Details, Team, Comp, Date, MatchID)"

    try:
        # Creates the table
        query = str("create table " + matchName + headerString)
        dbCursor.execute(query)

        # Inserts the tuples
        for tuple in data:
            dbCursor.execute(f"""INSERT INTO {matchName} VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", tuple)

        # Commits all executed querys to the .db-file
        dbConnection.commit()
    except sqlite3.Error as e:
        print(e)
        dbCursor.rollback()
        exit()

def deletedRow(tuple, list):
    rowNumber = tuple[7].lstrip("row: ")
    i=0
    while True:
        if list[i][0] == rowNumber:
            list.remove(list[i])
            break

  
if __name__ == "__main__":
    createTable()
    dbCursor.close()


"""Måste lägga till så att det är MM:SS istället för M:SS på matchtime, funkar om man ändrar [t]:mm till [tt]:mm
    Fungerar även med korrigeringen jag gjorde på koden rad 16-17
    Fixat totlei2022, inte resten"""