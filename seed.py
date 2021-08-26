from models import db, League, Team, Match, Player
from app import app
import json


db.drop_all()
db.create_all()

PremierLeague = League(id="39",name="premier_league")
Bundesliga = League(id="78",name="bundesliga")
LaLiga = League(id="140",name="la_liga")
# Add other leagues 


db.session.add_all([PremierLeague,Bundesliga,LaLiga])
db.session.commit()


def seed_teams_table(league_name):
    """  """
    standings = league_name.get_standings(league_name)
    for team in standings:
        id = team['team']['id']
        league_id = league_name.id
        name = team['team']['name']
        photo = team['team']['logo']
        rank = team['rank']
        points = team['points']
        games_played = team['all']['played']
        games_won = team['all']['win']
        games_drawn= team['all']['draw']
        games_lost = team['all']['lose']
        home_wins = team['home']['win']
        home_draws = team['home']['draw']
        home_losses = team['home']['lose']
        away_wins = team['away']['win']
        away_draws = team['away']['draw']
        away_losses = team['away']['lose']
        goal_diff = team['goalsDiff']
        goals_for = team['all']['goals']['for']    
        goals_against = team['all']['goals']['against']
         
        new_team = Team(id=id,name=name,photo=photo,rank=rank,points=points,games_played=games_played,games_won=games_won,games_drawn=games_drawn,games_lost=games_lost,home_wins=home_wins,home_draws=home_draws,home_losses=home_losses,away_wins=away_wins,away_draws=away_draws,away_losses=away_losses,goal_diff=goal_diff,goals_for=goals_for,goals_against=goals_against,league_id=league_id)
        
        db.session.add(new_team)
    db.session.commit()

def seed_players_table(league_name):
    """ Give league. Loop through league for each team id. Then call API via Team class method for active squad. Loop through squad """
    league_teams = Team.query.filter_by(league_id=f"{league_name.id}").all()
    print(league_teams)
    for team in league_teams:
        players = team.get_active_squad(team)
        team_id = players[0]["team"]["id"]
        team_name = players[0]["team"]["name"]
        players_list = players[0]["players"]
        for player in players_list:
            id = player["id"]
            name = player["name"]        
            age = player["age"]
            number = player["number"]
            position = player["position"]
            photo = player["photo"]
            
            new_player = Player(id=id,name=name,age=age,number=number,position=position,photo=photo,team_id=team_id,team_name=team_name)
            
            db.session.add(new_player)
        db.session.commit()
        
def seed_teams_then_players_tables(league_name):
    seed_teams_table(league_name)
    seed_players_table(league_name)
    
seed_teams_then_players_tables(PremierLeague)
    
def seed_matches_table(league_name):
    upcoming_matches = league_name.get_upcoming_matches(league_name)
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
  
  
  
def seed_teams_tables():
    leagues = League.query.all()
    for league in leagues:
        seed_teams_table(league)
        