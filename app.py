# from flask import Flask, render_template, redirect, session, flash
# from models import connect_db, db, User, Tweet
# from sqlalchemy.exc import IntegrityError
import requests
from secrets import API_FOOTBALL_KEY


def get_PL_table():
    
    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    querystring = {"league":"39","season":"2021"}

    headers = {
        'x-rapidapi-key': f"{API_FOOTBALL_KEY}",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    league_table = data['response'][0]['league']
    PL_table = league_table['standings']
    return PL_table

def get_PL_teams():
    """ Returns list of 20 PL teams in order of current standings """
    raw_table = get_PL_table()
    table = raw_table[0]
    teams = [team['team']['name'] for team in table]
    return teams