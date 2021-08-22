from models import db, League, Team
from app import app


db.drop_all()
db.create_all()

PremierLeague = League(api_id="39",name="premier_league")

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
        name = Team(api_id=id, name=name, league_id=PremierLeague.api_id)
        db.session.add(name)
    db.session.commit()
    
seed_teams_table()