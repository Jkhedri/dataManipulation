import sqlite3

databaseName = 'database'              # Databasename in string format
dbConnection = sqlite3.connect(databaseName+'.db') # Establishes database connection
dbCursor = dbConnection.cursor()    # Creates a query cursor

def drop(viewName):
        # Drops previous view of selected league if it already exists
    try:
        query = f"""DROP view {viewName}""";
        dbCursor.execute(query)
        dbConnection.commit()  
    except sqlite3.Error as e:
        print(f"""ROLLBACK: {viewName} view does not exists or other error.""")
        print("Error message:", e.args[0])
        dbConnection.rollback()
        pass

def fetchInteractions():
    try:
        query = """SELECT * FROM interactions""";  # Fetches a list of all tables in the database
        dbCursor.execute(query)
        interactions = dbCursor.fetchall()                            # Saves fetched table-names to variable 'tables'
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

