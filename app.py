from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Tweet
from sqlalchemy.exc import IntegrityError
import requests


url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"39","season":"2021"}

headers = {
    'x-rapidapi-key': "0c53816d30mshaf76a97a06df018p1a51f7jsn5f2149fe7ff0",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)