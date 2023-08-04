import requests
import csv

def getLeagueStats():
    #All urls will be based off of this one
    baseurl = "https://statsapi.web.nhl.com/api/v1"

    fullurl = baseurl + "/teams"
    teamreq = requests.get(fullurl)
    data = teamreq.json()

    teams = data.get("teams")

    #Header for the CSV
    header = ["team", "fullName", "birthDate", "currentAge", "birthCity", "birthCountry", "nationality", "height", "weight", "active", "captain", "alternateCaptain", "rookie", "shootsCatches", "rosterStatus", "primaryNumber", "position", "timeOnIce", "assists", "goals", "pim", "shots", "games", "hits", "powerPlayGoals", "powerPlayPoints", "powerPlayTimeOnIce", "evenTimeOnIce", "penaltyMinutes", "faceOffPct", "shotPct", "gameWinningGoals", "overTimeGoals", "shortHandedGoals", "shortHandedPoints", "shortHandedTimeOnIce", "blocked", "plusMinus", "points", "shifts", "timeOnIcePerGame", "evenTimeOnIcePerGame", "shortHandedTimeOnIcePerGame", "powerPlayTimeOnIcePerGame", "PTS/60"]
    
    #Writing the header to the CSV
    with open("LeagueStats" + '_2022-23.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(header)

    #Looping through teams
    for x in teams:
        teamID = x["id"]
        abbreviation = x["abbreviation"]

        fullurl2 = fullurl + "/" + str(teamID) + "/roster"
        rosterreq = requests.get(fullurl2)
        data2 = rosterreq.json()
        roster = data2.get("roster")

        #Looping through players in each team
        for person in roster:
            player = person.get("person")

            playerID = player["id"]
        
            fullurl3 = baseurl + "/people/" + str(playerID) + "?hydrate=stats(splits=statsSingleSeason)"
            playerreq = requests.get(fullurl3)
            data3 = playerreq.json()  

            info = data3.get("people")
            infodict = info[0]

            positionInfo = infodict["primaryPosition"]
        
            #Ignoring goalies (their stats are different)
            if positionInfo["abbreviation"] == "G":
                continue

            #Creating a stat row for each player. Some values are missing for certain players,
            #so the try/except prevents code from crashing.
            playerList = []
            playerList = [abbreviation, infodict["fullName"],infodict["birthDate"],infodict["currentAge"]]

            try: 
                playerList.append(infodict["birthCity"])
            except KeyError: 
                playerList.append("NA")

            try: 
                playerList.append(infodict["birthCountry"])
            except KeyError: 
                playerList.append("NA")

            playerList.append(infodict["nationality"])

            try:
                playerList.append(infodict["height"])
            except KeyError:
                playerList.append("NA")

            try:
                playerList.append(infodict["weight"])
            except KeyError:
                playerList.append("NA")

            playerList.extend([infodict["active"],infodict["captain"],infodict["alternateCaptain"],infodict["rookie"]])
            
            try:
                playerList.append(infodict["shootsCatches"])
            except KeyError:
                playerList.append("?")
            
            playerList.append(infodict["rosterStatus"])

            try: 
                playerList.append(infodict["primaryNumber"])
            except KeyError: 
                playerList.append(000)


            positionInfo = infodict["primaryPosition"]
            playerList.append(positionInfo["abbreviation"])

            statsList = infodict["stats"]
            statsListDict = statsList[0]    
            splits = statsListDict["splits"]

            #Convert time from mm:ss format to minutes.
            def get_hrs(time_str):
                mm, ss = time_str.split(":")
                return float(mm) + float(ss)/60

            #If a player's stats section is not available, set all to 0s, and write the final player list to the CSV.
            if splits == [ ]:
                zeroValues = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                playerList.extend(zeroValues)

                with open("LeagueStats" + '_2022-23.csv', 'a', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)

                    writer.writerow(playerList)

                continue
            #Write the final player list to the CSV.
            else:
                splitDict = splits[0]
                splitDictStats = splitDict['stat']
                dataValues = list(splitDictStats.values())
                playerList.extend(dataValues)
                
                #Creating Pts/60 Stat
                playerList.append(splitDictStats["points"]/(get_hrs(splitDictStats["timeOnIcePerGame"])*splitDictStats["games"])*60)

                with open("LeagueStats" + '_2022-23.csv', 'a', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)

                    writer.writerow(playerList)

getLeagueStats()
