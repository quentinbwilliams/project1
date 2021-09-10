from models.api_client import api_football
from flask_sqlalchemy import SQLAlchemy
import requests
from models.join_tables import db

season = 2021

class League(db.Model):
    """
    Model Class for leagues.
    Everything inherits from League
    """
    __tablename__="leagues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    photo=db.Column(db.Text)
    standings=db.Column(db.Text)
    teams = db.relationship('Team', backref='league', lazy=True)
    matches = db.relationship('Match', backref='league', lazy=True)
    
    @staticmethod
    def get_standings(self):
        """ Returns a list of each team in the league in the current order of standing """
        standings = api_football.api_call("standings",league=f"{self.id}",season=f"{season}")
        standings_nested = standings[0]['league']['standings']
        standings_list = standings_nested[0]
        return standings_list
    
    @staticmethod
    def get_upcoming_matches(self):
        """ Returns the next 30 competition fixtures """
        response = api_football.api_call("fixtures",next="30",league=f"{self.id}")
        self.matches = response
        return response
    
    @staticmethod
    def get_live_matches(self):
        """ Returns live matches or False if no matches are live in that league """
        response = api_football.api_call("fixtures",live="all",league=f"{self.id}")
        if response['results'] == 0:
            return False
        else:
            return response
        
    @staticmethod
    def get_current_round_matches(self):
        """ Returns the current round of fixtures for the league """
        response = api_football.api_call("fixtures/rounds", league=f"{self.id}",season=f"{season}",current="true")
        return response
    
    @staticmethod
    def get_scorers(self):
        """ Returns the top-scorers for the league """
        response = api_football.api_call("players/topscorers", season=f"{season}", league=f"{self.id}")
        return response
    
    @staticmethod
    def get_team_names_ids(self):
        """ Calls .get_standings(self) method; creates a list of tuples with each team name and id [(team_name, team_id),...] """
        table = self.get_standings(self)
        team_names_ids = [(team['team']['name'],team['team']['id']) for team in table]
        return team_names_ids
    

    @staticmethod
    def get_completed_matches(self):
        """ Returns all matches for current season in league that have status of FT (full-time) """
        response = api_football.api_call("fixtures",league=f"{self.id}",season=f"{season}",status="FT")
        return response
    