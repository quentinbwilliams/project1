from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from secrets import API_FOOTBALL_KEY
from season import season
import requests

bcrypt = Bcrypt()
db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

#############################
### LEAGUES x TEAMS MODEL ###
#############################

class LeaguesTeams(db.Model):
    __tablename__ = 'leagues_teams'
    id = db.Column(db.Integer, primary_key=True)
    leauge_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    league = db.relationship('League', backref='leagues_teams')
    team = db.relationship('Team', backref='leagues_teams')

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
    teams = db.relationship('Team', secondary='leagues_teams')
    
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
        return standings_array
    
    @staticmethod
    def get_upcoming_fixtures(self):
        """
        Returns the next 20 competition fixtures 
        """
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"next":"20","league":f"{self.id}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        fixtures = resjson['response']
        return fixtures
    
    @staticmethod
    def get_live_fixtures(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"live":"all","league":f"{self.id}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key':f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resjson = response.json()
        live_fixtures = resjson
        return live_fixtures
        
    @staticmethod
    def get_current_round_fixtures(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"
        querystring = {"league":f"{self.id}","season":f"{season}","current":"true"}
        headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
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
    players = db.Column(db.Text, unique=False, nullable=True)
    coaches = db.Column(db.Text, unique=False, nullable=True)
    leagues = db.relationship("League", secondary="leagues_teams")
    
    @staticmethod
    def get_player_stats(self):
        """  """ 
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {"team":f"{self.id}","season":f"{season}"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': f"{API_FOOTBALL_KEY}"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()
    
    @staticmethod
    def get_team_stats(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
        querystring = {"league":f"{self.league_id}","season":f"{season}", "team":f"{self.id}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()

    @staticmethod
    def get_players(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {"team":f"{self.id}","season":f"{season}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()
    
    @staticmethod
    def get_transfers(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/transfers"
        querystring = {"team":f"{self.id}","season":f"{season}"}
        headers = {'x-rapidapi-host': "api-football-v1.p.rapidapi.com",'x-rapidapi-key': f"{API_FOOTBALL_KEY}"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()
    
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
    first_name = db.Column(db.Text, nullable=False)
    
    @classmethod
    def register(cls, username, password, email, first_name):
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
            return cls(username=username, password=hashed_utf8, email=email, first_name=first_name)
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
