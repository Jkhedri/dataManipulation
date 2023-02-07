import string
from xmlrpc.client import boolean
import dbFunctions

class PremierLeagueQueries():
    def __init__(self):
        dbFunctions.unionView("Premier League")
        self.abbrTeams = {
            "AFC Bournemouth": "bou",
            "Arsenal": "ars",
            "Aston Villa": "avl",
            "Brentford": "bre",
            "Brighton and Hove Albion": "bri", ###
            "Chelsea": "che",       ###
            "Crysal Palace": "cry", ###
            "Everton": "eve",
            "Fulham": "ful",
            "Leeds United": "lee",   ###
            "Leicaster City": "lei",
            "Liverpool": "liv", ###
            "Manchester City": "mci",
            "Manchester United": "mun", ###
            "Newcastle United": "new",
            "Nottingham Forest": "nfo",
            "Southampton": "sou",
            "Tottenham Hotspur": "tot",
            "West Ham United": "whu",
            "Wolverhampton Wanderers": "wol"
        }
        self.events = {
            "Inkast": "Throw-in",
            "Nick": "Head",
            "Matchstart": "Period Start",
            "Avslut på mål": "Shot on target",
            "Mål": "Goal",
            "Hörna tilldelad": "Corner awarded",
            "Hörna": "Corner taken",
            "Frispark": "Free kick",
            "Inspark": "Goal kick",
            "Tilläggstid": "Additional time",
            "Gult kort": "yellow card", #CONTAINS
            "Rött kort": "Red card", ###
            "Byte ut": "Player off",
            "Byten": "Player in",
            "Offside": "Offside", ### EFTER 5e OKT 
            "Räddning": "Goalie save", ###
            "Ramträff": "Frame hit", ###
            "Målvaktsbox": "Goalie punch", ###
            "Matchslut": "Period end"
        }    
        self.timestamps = {
            "00:00":"1",
            "05:00":"1",
            "10:00":"1",
            "15:00":"1",
            "20:00":"1",
            "25:00":"1",
            "30:00":"1",
            "35:00":"1",
            "40:00":"1",
            "HT":"1",
            "45:00":"2",
            "50:00":"2",
            "55:00":"2",
            "60:00":"2",
            "65:00":"2",
            "70:00":"2",
            "75:00":"2",
            "80:00":"2",
            "85:00":"2",
            "FT":"2",
            
        }
        self.numMatches = dbFunctions.matchesCount("PremierLeague", "League")
    
    def exits(self,name):
        if name in self.abbrTeams:
            print(f"{name} exists!")

    def abbr(self,name):
        if name in self.abbrTeams:
            print(self.abbrTeams[name])

    def likelyhoodQuestion(self, start=string, end=string, question=string, answers=[]):
        half = self.timestamps[start]
        assert half == self.timestamps[end]
        if answers[0].upper() == "JA" and answers[1].upper() == "NEJ":              # JA/NEJ-FRÅGA
            moreThan = 0
            if "fler än" in question.lower() or "mer än" in question.lower():
                moreThan = [int(i) for line in question.splitlines()
                            for i in filter(str.isdigit, line.split())][0]

            return self.yesNo(start,end,question,half,moreThan)
        elif "HÄNDELSER" in question.upper():                                       # HÄNDELSER
            return self.eventQuestion(start,end,question,half,answers)
        else:
            return None, None

    def yesNo(self, timeStart=string, timeStop=string, question=string, half=string, moreThan=int):
        events = []
        for event in self.events.keys():
            if event.upper() in question.upper():
                if event.upper() == "NICK" and "planhalva" in question.lower():         #NICK PÅ NÅGONS PLANHALVA
                    pass
                else:
                    events.append(self.events[event])
        if len(events) == 0:
            print("Kan ej rätta '" + question + "'")
            return None, None
        else:
            print(events[0])
            if moreThan == 0:
                data = dbFunctions.fetchDataYesNo("Premier League", timeStart, timeStop, half, events[0])
                yes = len(data)
                answerRates = [yes/self.numMatches, 1-yes/self.numMatches]
                return self.convertToPercentagesAndGetDifficulty(answerRates)

            else:
                data = dbFunctions.fetchDataCount("Premier League", timeStart, timeStop, half, events[0])
                yeses = []
                for tuple in data:
                    if tuple[0] > moreThan:
                        yeses.append(tuple)
                yes = len(yeses)
                answerRates = [yes/self.numMatches, 1-yes/self.numMatches]
                return self.convertToPercentagesAndGetDifficulty(answerRates)

    def eventQuestion(self, timeStart=string, timeStop=string, question=string, half=string, answers=[]):
        numEvents = len(answers)-1
        events = []
        for answer in answers:
            if answer in self.events.keys():
                events.append(self.events[answer])
            else:
                print(answer, "finns inte med som giltigt event")
        if len(events) != len(answers)-1:
            print("Något av eventen fanns ej med, kontrollera stavning")
            return None, None
        else:
            if "FLEST" in question.upper():
                print("FLEST")          # self.fetchdatacountcompareevent, jämför för varje matchid och addera till en dictionary
                return None, None
            elif "SIST" in question.upper():
                data = dbFunctions.fetchDataFirstLast("Premier League", timeStart, timeStop, half, events, "Last")
                count = {}
                for event in events:
                    count[event] = 0
                for tuple in data:
                    count[tuple[1]] += 1
                answerRates = []
                for event in events:
                    answerRates.append(count[event]/self.numMatches)
                answerRates.append((self.numMatches-len(data))/self.numMatches)
                return self.convertToPercentagesAndGetDifficulty(answerRates)

            elif "FÖRST" in question.upper():
                data = dbFunctions.fetchDataFirstLast("Premier League", timeStart, timeStop, half, events, "First")
                count = {}
                for event in events:
                    count[event] = 0
                for tuple in data:
                    count[tuple[1]] += 1
                answerRates = []
                for event in events:
                    answerRates.append(count[event]/self.numMatches)
                answerRates.append((self.numMatches-len(data))/self.numMatches)
                return self.convertToPercentagesAndGetDifficulty(answerRates)
                
        
    def convertToPercentagesAndGetDifficulty(self, li):
        percentages = []
        totalDifficulty = 0
        for rate in li:
            percentages.append("{:.1%}".format(rate))
            totalDifficulty = totalDifficulty  + rate**2
        return percentages, totalDifficulty
                



        

if __name__ == "__main__":
    premierLeague = PremierLeagueQueries()
    print(premierLeague.numMatches)
    dbFunctions.dbConnection.close()


"""
Hade varit tvärnice att kunna ta ut information ur en google spreadsheet och returnera sannolikheten i spreadsheetet
Frågor av liknande typ har liknande upplägg och liknande svarsalternativ. Borde gå att ta in en sträng från spreadsheet
    och sedan använda "contains" osv. för att pinpointa vad det är för fråga och vad som behövs för att besvara den.
    Dictionaries är min vän
    Måste fixa väldigt många olika fall men det går
"""  """
    JA/NEJ-fråga. Intervall (ex. 0, 1, 2 eller fler / 0-3, 4-6 osv.). först/sist. Hemma/borta/oavgjort. Hemma/Borta/båda/inget. Händelser


    Kan kanske komma undan att ha databasen offentligt (eller semioffentligt) om jag enkrypterar den först och sen dekrypterar vid användning
    """