"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd

import requests

#from operator import truediv
#from celery import Celery
#from .models import Scores
#from . import db
#import requests
#import dash_html_components as html
#import pandas as pd
#import plotly.express as px
#import dash_core_components as dcc
#from dash import Dash




def create_dataframe():
    """Create Pandas DataFrame from local CSV."""
    """
    df = pd.read_csv('/Users/phongbui/Documents/GitHub/learn_python/Flask/project/data/311-calls.csv', parse_dates=["created"])
    df["created"] = df["created"].dt.date
    df.drop(columns=["incident_zip"], inplace=True)
    num_complaints = df["complaint_type"].value_counts()
    to_remove = num_complaints[num_complaints <= 30].index
    df.replace(to_remove, np.nan, inplace=True)
    return df
    """
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


    #db.session.add(leaderData)
    #Scores.query.filter(Scores.tournId == '004').delete()
    #db.session.bulk_insert_mappings(Scores,leaderData.to_dict(orient="records"))
    #db.session.commit()
    #return("Done")
    
    df = leaderData
    return df
