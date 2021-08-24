from requests.models import StreamConsumedError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from season import season
import requests

API_FOOTBALL_KEY = "0c53816d30mshaf76a97a06df018p1a51f7jsn5f2149fe7ff0"

bcrypt = Bcrypt()
db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

####################
### LEAGUE MODEL ###
####################

class League(db.Model):
    """
    Model Class for leagues.
    Everything inherits from league
    """
    __tablename__="leagues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    photo=db.Column(db.Text)
    standings=db.Column(db.Text)
    teams = db.relationship('Team', backref='league', lazy=True)
    matches = db.Column(db.Text)
    # matches = db.relationship('Match', backref='league', lazy=True)
    
    @staticmethod
    def get_standings(self):
        """  """
        url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        querystring = {"season":f"{season}","league":f"{self.id}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        standings = resjson['response']
        standings_nested = standings[0]['league']['standings']
        standings_array = standings_nested[0]
        self.standings = standings_array
        return standings_array
    
    @staticmethod
    def get_upcoming_matches(self):
        """
        Returns the next 30 competition fixtures 
        """
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"next":"30","league":f"{self.id}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        response = resjson['response']
        data = response
        self.matches = data
        return data
    
    @staticmethod
    def get_live_matches(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"live":"all","league":f"{self.id}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key':f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        live_fixtures = resjson
        if live_fixtures['results'] == 0:
            return False
        else:
            return live_fixtures
        
    @staticmethod
    def get_current_round_matches(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"
        querystring = {"league":f"{self.id}","season":f"{season}","current":"true"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        current_round = resjson['response']
        return current_round
    
    @staticmethod
    def get_scorers(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        querystring = {"season":f"{season}","league":f"{self.id}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        scorers = resjson['response']
        return scorers
    
    @staticmethod
    def get_team_names_ids(self):
        table = self.get_standings(self)
        team_names_ids = [(team['team']['name'],team['team']['id']) for team in table]
        return team_names_ids
   
##################    
### TEAM MODEL ###
##################

class Team(db.Model):
    """
    Contains info on teams and methods to view dynamic info
    """
    __tablename__="teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    photo=db.Column(db.Text)
    players = db.Column(db.Text, unique=False, nullable=True)
    coach = db.Column(db.Text, unique=False, nullable=True)
    player_stats = db.Column(db.Text)
    team_stats = db.Column(db.Text)
    transfers = db.Column(db.Text)
    # Fans = Number of users who favorite this team
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    
    # STATS BELOW
    shots_on_goal=db.Column(db.Integer)
    shots_off_goal=db.Column(db.Integer)
    shots_blocked=db.Column(db.Integer)
    shots_inside_box=db.Column(db.Integer)
    shots_outside_box=db.Column(db.Integer)
    fouls=db.Column(db.Integer)
    corner_kicks=db.Column(db.Integer)
    offsides_total=db.Column(db.Integer)
    possession_percent=db.Column(db.Integer)
    cards_yellow=db.Column(db.Integer)
    cards_red=db.Column(db.Integer)
    goalkeeper_saves=db.Column(db.Integer)
    passes_total=db.Column(db.Integer)
    passes_accurate=db.Column(db.Integer)
    passes_percent_accurate=db.Column(db.Integer)
    
    
    @staticmethod
    def get_player_stats(self):
        """  """ 
        from secrets import API_FOOTBALL_KEY
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {"team":f"{self.id}","season":f"{season}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        res = requests.request("GET", url, headers=headers, params=querystring)
        resjson=res.json()
        response = resjson['response']
        self.player_stats = response
        return response
    
    @staticmethod
    def get_team_stats(self):
        from secrets import API_FOOTBALL_KEY
        url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
        querystring = {"league":f"{self.league_id}","season":f"{season}", "team":f"{self.id}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        res = requests.request("GET", url, headers=headers, params=querystring)
        resjson=res.json()
        response = resjson['response']
        self.team_stats = response
        return response

    @staticmethod
    def get_players(self):
        from secrets import API_FOOTBALL_KEY
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {"team":f"{self.id}","season":f"{season}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        res = requests.request("GET", url, headers=headers, params=querystring)
        resjson=res.json()
        response = resjson['response']
        self.players = response
        return response
    
    @staticmethod
    def get_transfers(self):
        from secrets import API_FOOTBALL_KEY
        url = "https://api-football-v1.p.rapidapi.com/v3/transfers"
        querystring = {"team":f"{self.id}","season":f"{season}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        res = requests.request("GET", url, headers=headers, params=querystring)
        resjson=res.json()
        response = resjson['response']
        self.transfers = response
        return response
    
####################
### MATCH  MODEL ###
####################

class Match(db.Model):
    """
    Match represents a relationship between two Teams and a League.
    MANY to MANY relationship between Match and Team:
    --> Each match has MANY teams -- exactly two
    --> Each team has MANY matches (undefined)
    ONE to MANY relationship between League and Match:
    --> Each Match belongs to exactly ONE League
    --> Each league has many matches (undefined)
    """
    __tablename__="matches"
    id=db.Column(db.Integer,primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    date=db.Column(db.Text)
    referee=db.Column(db.Text)
    home = db.Column(db.Text)
    away = db.Column(db.Text)
    ht_score = db.Column(db.Text,nullable=True)
    ft_score = db.Column(db.Text,nullable=True)
    et_score = db.Column(db.Text,nullable=True)
    
class Player(db.Model):
    """
    
    """
    __tablename__='players'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    age=db.Column(db.Integer)
    nationality=db.Column(db.Text)
    photo=db.Column(db.Text)
    team=db.Column(db.Text)
    
    # STATS BELOW
    position=db.Column(db.Text)
    appearences=db.Column(db.Integer)
    minutes_played=db.Column(db.Integer)
    shots_on_goal=db.Column(db.Integer)
    shots_total=db.Column(db.Integer)
    goals_total=db.Column(db.Integer)
    goals_conceded=db.Column(db.Integer)
    assists=db.Column(db.Integer)
    saves=db.Column(db.Integer)
    passes_total=db.Column(db.Integer)
    passes_key=db.Column(db.Integer)
    passing_accuracy=db.Column(db.Integer)
    duels_attempted=db.Column(db.Integer)
    duels_successful=db.Column(db.Integer)
    dribbles_attempts=db.Column(db.Integer)
    dribbles_successful=db.Column(db.Integer)
    dribbles_past=db.Column(db.Integer)
    fouls_drawn=db.Column(db.Integer)
    fouls_commited=db.Column(db.Integer)
    cards_yellow=db.Column(db.Integer)
    cards_red=db.Column(db.Integer)
    penalties_won=db.Column(db.Integer)
    penalties_commited=db.Column(db.Integer)
    penalties_scored=db.Column(db.Integer)
    penalties_missed=db.Column(db.Integer)
    penalties_saved=db.Column(db.Integer)    
    
##################
### USER MODEL ###
##################
    
class User(db.Model):
    """
    User model should contain:
    Data:
    --> Favorite team
    --> Username
    --> Email
    --> Password
    --> Name
    --> Bio
    --> Picture
    Methods:
    --> Register
    --> Authenticate
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    favorite_team = db.Column(db.Text)
    following_leagues = db.Column(db.Text)
    following_teams = db.Column(db.Text)
    following_players = db.Column(db.Text)
    
    @classmethod
    def register(cls, username, password, email):
        """Register user with hashed password and return user"""
        # check if username exists in database
        username_exists = User.query.filter_by(username=username).first()
        # check if email exists in database
        email_exists = User.query.filter_by(email=email).first()
        if not username_exists and not email_exists:
            # hash password with bcrpyt
            hashed = bcrypt.generate_password_hash(password)
            # turn bytestring into utf8 string
            hashed_utf8 = hashed.decode("utf8")
            # return instance of user w/ username and hashed password            
            return cls(username=username, password=hashed_utf8, email=email)
        elif username_exists:
            # Should return F but let them know why
            return 'username already exists'
        elif email_exists:
            # Should return F but let them know why
            return 'that email is already registered with an account'
        
    @classmethod
    def authenticate(cls, username, password, email):
        """ Validate that user exists & password is correct. If valid, return user. Else, return false """
        # check if username exists in database
        username_exists = User.query.filter_by(username=username).first()
        # check if email exists in database
        email_exists = User.query.filter_by(email=email).first()
        # if the username is in the table AND bcrypt returns the same hash for the password stored in the user table and password from form, return authorized user instance
        if username_exists and email_exists and bcrypt.check_password_hash(username_exists.password, password):
            # return user instance
            return username_exists
        else:
            # if username is not in db or password does not match, deny
            return False    
