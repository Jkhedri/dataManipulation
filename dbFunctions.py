import sqlite3

databaseName = 'tnlbc'              # Databasename in string format
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
                              
def unionView(leagueName):
                # Creates a view consisting of all events that have occured in a selected league
    leagueNameNoSpace = leagueName.replace(" ", "")
    drop(leagueNameNoSpace)
    try:
        query = """SELECT name FROM sqlite_master WHERE type='table' ORDER BY name""";  # Fetches a list of all tables in the database
        dbCursor.execute(query)
        tables = dbCursor.fetchall()                            # Saves fetched table-names to variable 'tables'
        dbConnection.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()
    try:
        query = str(f"""Create view {leagueNameNoSpace} AS """ + allTablesUnionString(tables, leagueName))
        dbCursor.execute(query)
        dbConnection.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

                                # Creates a view with all events commited by a specific team
def specificTeamEventsView(teamName, leagueName):
    leagueNameNoSpace = leagueName.replace(" ", "")
    teamNameNoSpace = teamName.replace(" ", "")
    drop(teamNameNoSpace)
    try:
        query = str(f"""Create view {teamNameNoSpace} AS Select * from {leagueNameNoSpace} where Team like '{teamName}'""")
        dbCursor.execute(query)
        dbConnection.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def matchesCount(viewName, leagueOrTeam):
    try:
        if leagueOrTeam == "League":
            query = f"""SELECT EventType,MatchID FROM {viewName} WHERE EventType='Period start' and period='1'""";  # Fetches a list of all tables in the database
        elif leagueOrTeam == "Team":
            query = f"""SELECT EventType,MatchID FROM {viewName} WHERE EventType='Period start'""";        # HAS TO BE MADE SO THAT THE MATCHID HAS IS EITHER ARS...#### or ...ARS####
        dbCursor.execute(query)
        allStarts = dbCursor.fetchall()                            # Saves fetched table-names to variable 'tables'
        dbConnection.commit()
        return len(allStarts)
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def leagueOrTeam(viewName, nameList):
    for name in nameList:
        if viewName.lower() == name.replace(" ", "").lower():
            return "Team"
    return "League"
                    
def allTablesUnionString(nameList, league):
                    # Creates string used for sql-command where a league view is created
    returnString = ""
    for attribute in nameList:
        if len(nameList) == 1:
            returnString += f"""Select Period,MatchTime,EventType,Details,Date,Team,MatchID from {attribute[0]} where comp = '{league}'"""
        elif attribute == nameList[-1]:
            returnString += f"""Select Period,MatchTime,EventType,Details,Date,Team,MatchID from {attribute[0]} where comp = '{league}'"""
        else:
            returnString += f"""Select Period,MatchTime,EventType,Details,Date,Team,MatchID from {attribute[0]} where comp = '{league}' UNION """
    return returnString

def fetchMatches():
    try:
        query = """SELECT name FROM sqlite_master WHERE type='table' ORDER BY name""";  # Fetches a list of all tables in the database
        dbCursor.execute(query)
        matches = dbCursor.fetchall()                            # Saves fetched table-names to variable 'tables'
        dbConnection.commit()
        return matches
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def fetchDataYesNo(comp, start, stop, half, event):
    try:
        compNameNoSpace = comp.replace(" ", "")
        if "HT" in stop or "FT" in stop:
            query = f"select MatchTime,EventType,Details,Date,Team,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and EventType='{event}' group by matchID";
        else:
            query = f"select MatchTime,EventType,Details,Date,Team,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and EventType='{event}' group by matchID";
        dbCursor.execute(query)
        data = dbCursor.fetchall()
        dbConnection.commit()
        return data
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def fetchDataCount(comp, start, stop, half, event):
    try:
        compNameNoSpace = comp.replace(" ", "")
        if "HT" in stop or "FT" in stop:
            query = f"select count(matchtime) as TheCount,EventType,Date,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and EventType='{event}' group by matchID";
        else:
            query = f"select count(matchtime) as TheCount,EventType,Date,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and EventType='{event}' group by matchID";
        dbCursor.execute(query)
        data = dbCursor.fetchall()
        dbConnection.commit()
        return data
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def fetchDataCountByTeam(comp, start, stop, half, event):
    try:
        compNameNoSpace = comp.replace(" ", "")
        if "HT" in stop or "FT" in stop:
            query = f"select count(matchtime) as TheCount,EventType,Date,Team,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and EventType='{event}' group by matchID, Team";
        else:
            query = f"select count(matchtime) as TheCount,EventType,Date,Team,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and EventType='{event}' group by matchID, Team";
        dbCursor.execute(query)
        data = dbCursor.fetchall()
        dbConnection.commit()
        return data
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def fetchDataEventCount(comp, start, stop, half, event):
    try:
        compNameNoSpace = comp.replace(" ", "")
        if "HT" in stop or "FT" in stop:
            query = f"select count(matchtime) as TheCount,EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and EventType='{event}' group by matchID";
        else:
            query = f"select count(matchtime) as TheCount,EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and EventType='{event}' group by matchID";
        dbCursor.execute(query)
        data = dbCursor.fetchall()
        dbConnection.commit()
        return data
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def fetchDataFirstLast(comp, start, stop, half, events, firstOrLast):
    try:
        compNameNoSpace = comp.replace(" ", "")
        eventString = ""
        for event in events:
            if event == events[0]:
                eventString += f"EventType='{event}'"
            else:
                eventString += f" or EventType='{event}'"
        if firstOrLast == "First":
            if "HT" in stop or "FT" in stop:
                query = f"select min(MatchTime),EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and ({eventString}) group by matchID";
            else:
                query = f"select min(MatchTime),EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and ({eventString}) group by matchID";
        elif firstOrLast == "Last":
            if "HT" in stop or "FT" in stop:
                query = f"select max(MatchTime),EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and ({eventString}) group by matchID";
            else:
                query = f"select max(MatchTime),EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and ({eventString}) group by matchID";
        dbCursor.execute(query)
        data = dbCursor.fetchall()
        dbConnection.commit()
        return data
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()

def fetchDataCountCompareEvents(comp, start, stop, half, events):
    try:
        compNameNoSpace = comp.replace(" ", "")
        eventString = ""
        for event in events:
            if event == events[0]:
                eventString += f"EventType='{event}'"
            else:
                eventString += f" or EventType='{event}'"
        if "HT" in stop or "FT" in stop:
            query = f"select count(MatchTime),EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and ({eventString}) group by matchID, EventType";
        else:
            query = f"select count(MatchTime),EventType,MatchID from {compNameNoSpace} where Period='{half}' and matchtime>'{start}' and matchtime<'{stop}' and ({eventString}) group by matchID, EventType";
        dbCursor.execute(query)
        data = dbCursor.fetchall()
        dbConnection.commit()
        return data
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        dbConnection.rollback()
        exit()



if __name__ == "__main__":
    unionView("Premier League")
    dbConnection.close()