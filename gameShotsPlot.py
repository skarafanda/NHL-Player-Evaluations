import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
from datetime import date

#In the API, games that are in progress are first, games that have finished are at the bottom. 

#Returns a list of all Game IDs today (at the date when the function is called).
def getGamePk():
    gameIds = []

    baseurl = "https://statsapi.web.nhl.com/api/v1/schedule?date=" + date.today().strftime("%Y-%m-%d")
    teamreq = requests.get(baseurl)
    data = teamreq.json()
    dates = data.get("dates")
    datesDict = dates[0]
    games = datesDict.get("games")

    for i in games:
        gameIds.append(str(i["gamePk"]))
    print(gameIds)

#Returns the Game ID given the team name of one of the teams and the date of the game in YYYY-MM-DD format.
def getGamePk(fullTeamName, date):
    #baseurl = "https://statsapi.web.nhl.com/api/v1/schedule?date=" + date.today().strftime("%Y-%m-%d")
    baseurl = "https://statsapi.web.nhl.com/api/v1/schedule?date=" + date
    teamreq = requests.get(baseurl)
    data = teamreq.json()
    dates = data.get("dates")
    datesDict = dates[0]
    games = datesDict.get("games")

    for i in games:
        if (fullTeamName in i["teams"]["away"]["team"]["name"]) or fullTeamName in i["teams"]["home"]["team"]["name"]:
            return str(i["gamePk"])

#Returns a list of 2 dictionaries -- one for the home team and one for the away team -- and a time string. 
# In these dictionaries, player names are mapped to "shots", and "goals" dictionaries 
# that are composed of a list of tuples (shot coords).
def getShotCoordinates(gameId):
    print(gameId)

    homeRight = ["CBJ", "NJD", "NYI", "PIT", "BOS", "BUF", "OTT", "TBL", "ARI", "NSH", "STL", "ANA", "EDM", "SJS", "SEA"]

    baseurl = "https://statsapi.web.nhl.com/api/v1/game/" + gameId + "/feed/live"
    teamreq = requests.get(baseurl)
    data = teamreq.json()
    gameData = data.get("gameData")

    homeTeam = gameData["teams"]["home"]["triCode"]
    awayTeam = gameData["teams"]["away"]["triCode"]

    homeDict = {homeTeam: {}}
    awayDict = {awayTeam: {}}

    # for i in gameData["players"].values():
    #     if i["currentTeam"]["name"] == homeTeam:
    #         homeRoster.append(i["fullName"])

    liveData = data.get("liveData")
    plays = liveData["plays"]
    allPlays = plays["allPlays"]          
    for i in range(len(allPlays)):
        if allPlays[i]['result']['eventTypeId'] == "SHOT":
            x = allPlays[i].get("players")[0]
            #if x["player"]["fullName"] in homeRoster:
            if allPlays[i].get("team")["triCode"] == homeTeam:
                if homeTeam in homeRight:
                    if allPlays[i]["about"]["ordinalNum"] in ["1st", "3rd", "2OT", "4OT", "6OT", "8OT"]:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["shots"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))], "goals": []}
                            
                    else:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["shots"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])], "goals": []}
                else:
                    if allPlays[i]["about"]["ordinalNum"] in ["2nd", "OT", "3OT", "5OT", "7OT", "9OT"]:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["shots"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))], "goals": []}
                    else:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["shots"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])], "goals": []}
            else:
                if homeTeam in homeRight:
                    if allPlays[i]["about"]["ordinalNum"] in ["1st", "3rd", "2OT", "4OT", "6OT", "8OT"]:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["shots"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))], "goals": []}
                    else:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["shots"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])], "goals": []}
                else:
                    if allPlays[i]["about"]["ordinalNum"] in ["2nd", "OT", "3OT", "5OT", "7OT", "9OT"]:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["shots"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))], "goals": []}
                    else:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["shots"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])], "goals": []}

        elif allPlays[i]['result']['eventTypeId'] == "GOAL":
            x = allPlays[i].get("players")[0]
            if allPlays[i].get("team")["triCode"] == homeTeam:
                if homeTeam in homeRight:
                    if allPlays[i]["about"]["ordinalNum"] in ["1st", "3rd", "2OT", "4OT", "6OT", "8OT"]:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["goals"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))]}
                    else:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["goals"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])]}
                else:
                    if allPlays[i]["about"]["ordinalNum"] in ["2nd", "OT", "3OT", "5OT", "7OT", "9OT"]:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["goals"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))]}
                    else:
                        if x["player"]["fullName"] in homeDict[homeTeam].keys():
                            homeDict[homeTeam][x["player"]["fullName"]]["goals"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            homeDict[homeTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])]}

            else:
                if homeTeam in homeRight:
                    if allPlays[i]["about"]["ordinalNum"] in ["1st", "3rd", "2OT", "4OT", "6OT", "8OT"]:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["goals"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))]}
                    else:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["goals"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])]}
                else:
                    if allPlays[i]["about"]["ordinalNum"] in ["2nd", "OT", "3OT", "5OT", "7OT", "9OT"]:
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["goals"].append((-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"])))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(-(allPlays[i].get("coordinates")["x"]), -(allPlays[i].get("coordinates")["y"]))]}
                    else: 
                        if x["player"]["fullName"] in awayDict[awayTeam].keys():
                            awayDict[awayTeam][x["player"]["fullName"]]["goals"].append((allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"]))
                        else:
                            awayDict[awayTeam][x["player"]["fullName"]] = {"shots": [], "goals": [(allPlays[i].get("coordinates")["x"], allPlays[i].get("coordinates")["y"])]}
    
    timeStr = ""
    if liveData["linescore"]["currentPeriodTimeRemaining"] == "Final" and (liveData["linescore"]["currentPeriodOrdinal"][1:] == "OT"):
        timeStr = liveData["linescore"]["currentPeriodTimeRemaining"] + " (" + liveData["linescore"]["currentPeriodOrdinal"] + ")"
    elif liveData["linescore"]["currentPeriodTimeRemaining"] == "Final":
        timeStr = liveData["linescore"]["currentPeriodTimeRemaining"]
    else: 
        timeStr = (liveData["linescore"]["currentPeriodOrdinal"] + " | " + liveData["linescore"]["currentPeriodTimeRemaining"] + " Remaining")

    return([homeDict, awayDict, timeStr])

#getShotCoordinates(getGamePk("Arizona Coyotes", "2022-11-27"))

def plotShots(shotList):
    x = [0.0, 69.0, -69.0, 69.0, -69.0, 20.0, -20.0, 20.0, -20.0]
    y = [0.0, 22.0, -22.0, -22.0, 22.0, -22.0, -22.0, 22.0, 22.0]
    x_adjusted = [x2 + 100 for x2 in x] #translate to positive coordinate system
    y_adjusted = [y2 + 42 for y2 in y]

    draw_circle_1 = plt.Circle((100, 42), 15, fill=False, color='salmon', zorder=-1) #centre ice 
    draw_circle_2 = plt.Circle((169, 64), 15, fill=False, color='salmon', zorder=-1) #top right
    draw_circle_3 = plt.Circle((169, 20), 15, fill=False, color='salmon', zorder=-1) #bottom right
    draw_circle_4 = plt.Circle((31, 64), 15, fill=False, color='salmon', zorder=-1) #top left
    draw_circle_5 = plt.Circle((31, 20), 15, fill=False, color='salmon', zorder=-1) #bottom left

    # Create crease
    crease_1 = Rectangle((11, 38), 4, 8, angle=0.0, fc='lavender', alpha=0.75, zorder=-2)
    crease_2 = Rectangle((15, 38), 0.5, 8, angle=0.0, fc='lavender', alpha=0.75, zorder=-2)
    crease_3 = Arc((15.5, 42), width=3, height=7.5, angle=0.0, theta1=270.0, theta2=90.0, fc='lavender', alpha=0.75, zorder=-2)
    crease_4 = Rectangle((185, 38), 4, 8, angle=0.0, fc='lavender', alpha=0.75, zorder=-2)
    crease_5 = Rectangle((184.5, 38), 0.5, 8, angle=0.0, fc='lavender', alpha=0.75, zorder=-2)
    crease_6 = Arc((184.5, 42), width=3, height=7.5, angle=0.0, theta1=90.0, theta2=270.0, fc='lavender', alpha=0.75, zorder=-2)

    fig, ax = plt.subplots(figsize=(16, 6.8))
    ax.set_xlim([0, 200])
    ax.set_ylim([0, 86])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axvline(75, color='lightskyblue', linewidth=5, zorder=-1)
    ax.axvline(125, color='lightskyblue', linewidth=5, zorder=-1)
    ax.axvline(100, color='salmon', linewidth=5, zorder=-1)
    ax.axvline(11, color='salmon', linewidth=3, zorder=-1)
    ax.axvline(189, color='salmon', linewidth=3, zorder=-1)
    ax.add_artist(draw_circle_1)
    ax.add_artist(draw_circle_2)
    ax.add_artist(draw_circle_3)
    ax.add_artist(draw_circle_4)
    ax.add_artist(draw_circle_5)
    ax.add_artist(crease_1)
    ax.add_artist(crease_2)
    ax.add_artist(crease_3)
    ax.add_artist(crease_4)
    ax.add_artist(crease_5)
    ax.add_artist(crease_6)
    ax.scatter(x_adjusted, y_adjusted, s=100, c='salmon', linewidths=1, edgecolors='w', zorder=-2)

    homeShots = shotList[0]
    awayShots = shotList[1]
    timeStr = shotList[2]

    a = list(homeShots.values())[0]
    b = list(awayShots.values())[0]

    homeGoals = 0
    awayGoals = 0

    for i in a.keys():
        for s in a[i]["shots"]:
            #print(s[0], s[1])
            ax.scatter(-abs(s[0]) + 100, s[1] + 42, c="darkseagreen", linewidths=1, marker="s", edgecolor="black", s=30)
            plt.text(-abs(s[0]) + 100, s[1] + 43, i.split(" ", 1)[-1], fontsize=6)
        for g in a[i]["goals"]:
            ax.scatter(-abs(g[0]) + 100, g[1] + 42, c="lime", linewidths=2, marker="^", edgecolor="black", s=50, zorder=1)
            plt.text(-abs(g[0]) + 100, g[1] + 43, i.split(" ", 1)[-1], fontsize=6, zorder=1)
            homeGoals = homeGoals + 1

    for i in b.keys():
        for s in b[i]["shots"]:
            #print(s[0], s[1])
            ax.scatter(abs(s[0]) + 100, s[1] + 42, c="lightcoral", linewidths=1, marker="s", edgecolor="black", s=30)
            plt.text(abs(s[0]) + 100, s[1] + 43, i.split(" ", 1)[-1], fontsize=6)
        for g in b[i]["goals"]:
            ax.scatter(abs(g[0]) + 100, g[1] + 42, c="yellow", linewidths=2, marker="^", edgecolor="black", s=50, zorder=1)
            plt.text(abs(g[0]) + 100, g[1] + 43, i.split(" ", 1)[-1], fontsize=6, zorder=1)
            awayGoals = awayGoals + 1

    plt.text(2, 40, list(homeShots.keys())[0], fontsize=10, rotation="vertical", fontweight="bold")
    plt.text(195, 40, list(awayShots.keys())[0], fontsize=10, rotation=270, fontweight="bold")
    plt.text(100, 87, list(homeShots.keys())[0] + " - " + str(homeGoals) + "   " + list(awayShots.keys())[0] + " - " + str(awayGoals), fontsize=10, fontweight="bold", horizontalalignment="center")
    plt.text(100, 91, timeStr, fontsize=10, fontweight="bold", horizontalalignment="center")
    plt.show()

#plotShots(getShotCoordinates(getGamePk("New York Rangers", "2022-05-03"))) #2021030141 <- gameID for OT game (for testing)
plotShots(getShotCoordinates(getGamePk("Arizona Coyotes", "2022-11-27")))