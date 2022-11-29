
import numpy as np
import pandas as pd
import requests

def tournamentData():

    url = "https://live-golf-data.p.rapidapi.com/leaderboard"

    querystring = {"tournId":"004","year":"2022"}

    headers = {
    'x-rapidapi-host': "live-golf-data.p.rapidapi.com",
    'x-rapidapi-key': "61ac0c86e6msh348d8e602f15c14p1d225bjsn6c2420358e9e"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    output = response.json()

    headerData = pd.json_normalize(data=output)
    leaderData = pd.json_normalize(data=output['leaderboardRows'], record_path=['rounds'], meta=['lastName', 'firstName','playerId', 'status', 'total', 'currentRoundScore', 'position'])
    leaderData['tournId'] = headerData.loc[0,'tournId']
    leaderData['year'] = headerData.loc[0,'year']
    leaderData['tournStatus'] = headerData.loc[0,'status']
    leaderData['currentRound'] = headerData.loc[0,'roundId.$numberInt']
    leaderData['currentRoundStatus'] = headerData.loc[0,'roundStatus']
    leaderData['roundId'] = leaderData['roundId.$numberInt']
    leaderData['strokes'] = leaderData['strokes.$numberInt']

    leaderData=leaderData[['tournId','year','tournStatus','currentRound','currentRoundStatus','playerId','lastName','firstName','position','total','roundId','scoreToPar','strokes']]
    leaderData = leaderData[leaderData['roundId']== '4']

    leaderData.to_csv("golf.csv")
    
    pass
