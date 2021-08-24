from models import db, League, Team, Match
from app import app
import json


db.drop_all()
db.create_all()

PremierLeague = League(id="39",name="premier_league")

db.session.add(PremierLeague)
db.session.commit()

def clean_standings():
    """ Calls get_standings from league and prepares league standings for iteration """
    standings_ditry = PremierLeague.get_standings(PremierLeague)
    standings_data = standings_ditry[0]['league'] ['standings']
    standings_clean = standings_data[0]
    return standings_clean

def extract_team_names_ids():
    """ Returns an array of tuples matching team name with team id """
    table = clean_standings()
    team_names_ids = [(team['team']['name'],team['team']['id']) for team in table]
    return team_names_ids

def seed_teams_table():
    """  """
    team_names_ids = PremierLeague.get_team_names_ids(PremierLeague)
    for name, id in team_names_ids:
        name = Team(id=id, name=name, league_id=PremierLeague.id)
        db.session.add(name)
    db.session.commit()
    
def seed_matches():
    upcoming_matches = PremierLeague.get_upcoming_matches(PremierLeague)
    for match in upcoming_matches:
        id = match['fixture']['id']
        league_id = match['league']['id']
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        date = match['fixture']['date']
        referee = match['fixture']['referee']
        ht_score = (match['score']['halftime']['home'],match['score']['halftime']['away'])
        ft_score = (match['score']['halftime']['home'],match['score']['halftime']['away'])
        et_score = (match['score']['halftime']['home'],match['score']['halftime']['away'])
        new_match = Match(id=id,league_id=league_id,home=home,away=away,ht_score=ht_score,ft_score=ft_score,et_score=et_score,date=date,referee=referee)
        db.session.add(new_match)
    db.session.commit()
    