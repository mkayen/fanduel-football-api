import urllib3
from bs4 import BeautifulSoup
from pymongo import MongoClient
import credentials

client = MongoClient(credentials.databaseUri)
db = client['numberfire-football']
collection = db['players']

players = []
playerNamesTotal = []
playerStatsTotal = []

http = urllib3.PoolManager();
r = http.request('GET', 'http://www.numberfire.com/nfl/fantasy/fantasy-football-projections')

soup = BeautifulSoup(r.data, 'html.parser')

playerNames = soup.find_all("td", {"class" : "player"})

for player in playerNames:
	playerName = []
	name = player.find("span", {"class" : "full"}).get_text();
	teamAndPosition = player.get_text()[player.get_text().index('('):player.get_text().index(')')+1];
	position = teamAndPosition[1:3]
	team = teamAndPosition[teamAndPosition.index(',')+2:teamAndPosition.index(')')]
	playerName.append(name)
	playerName.append(position)
	playerName.append(team)
	playerNamesTotal.append(playerName)
	
bodyWithAllTheStats = soup.find_all("tbody", {"class" : "projection-table__body"})[1]
playerStats = bodyWithAllTheStats.find_all("tr")

for player in playerStats:
    playerStat = []
    fanduel_fp = player.find("td", {"class" : "fanduel_fp"}).get_text().strip()
    fanduel_cost =  player.find("td", {"class" : "fanduel_cost"}).get_text().strip()[1:]
    playerStat.append(fanduel_fp)
    playerStat.append(fanduel_cost)
    playerStatsTotal.append(playerStat)

db.players.delete_many({})

i=0
while i < len(playerNames):
    player = playerNamesTotal[i] + playerStatsTotal[i]
    post = {"name": playerNamesTotal[i][0],
            "position": playerNamesTotal[i][1],
            "team": playerNamesTotal[i][2],
            "fanduel_fp": playerStatsTotal[i][0],
            "fanduel_cost": playerStatsTotal[i][1]}
    db['players'].insert_one(post)
    i+=1