from models.join_tables import db
from models.league import season
from models.api_client import api_football

class Team(db.Model):
    """
    Contains info on teams and methods to view dynamic info
    """
    __tablename__="teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    players = db.relationship('Player', backref='team')
    coach = db.Column(db.Text, unique=False, nullable=True)
    photo=db.Column(db.Text)
    rank = db.Column(db.Integer)
    points = db.Column(db.Integer)
    games_played=db.Column(db.Integer)
    games_won=db.Column(db.Integer)
    games_drawn=db.Column(db.Integer)
    games_lost=db.Column(db.Integer)
    home_wins=db.Column(db.Integer)
    home_draws=db.Column(db.Integer)
    home_losses=db.Column(db.Integer)
    away_wins=db.Column(db.Integer)
    away_draws=db.Column(db.Integer)
    away_losses=db.Column(db.Integer)
    goal_diff = db.Column(db.Integer)
    goals_for = db.Column(db.Integer)
    goals_against = db.Column(db.Integer)
    player_stats = db.Column(db.Text, nullable=True)
    team_stats = db.Column(db.Text)
    transfers = db.Column(db.Text)
    
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
    def get_active_squad(self):
        """ Returns all current squad players """
        response = api_football.api_call("players/squads", team=f"{self.id}")
        return response
    
    @staticmethod
    def get_player_stats(self):
        """ Returns stats current team players """ 
        response = api_football.api_call("players", season=f"{season}", team=f"{self.id}")
        return response
    
    @staticmethod
    def get_team_stats(self):
        """ Returns all stats for a team in the current season and league """
        response = api_football.api_call("teams/statistics", season=f"{season}", league=f"{self.league_id}", team=f"{self.id}")
        return response
    
    @staticmethod
    def get_transfers(self):
        response = api_football.api_call("transfers", season=f"{season}", team=f"{self.id}")
        return response