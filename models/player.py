from models.join_tables import db
from models.league import season
from models.team import Team
from models.api_client import api_football


class Player(db.Model):
    """ MANY Players to ONE Team
    """
    __tablename__='players'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    age=db.Column(db.Integer)
    nationality=db.Column(db.Text)
    photo=db.Column(db.Text)
    team_id=db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_name=db.Column(db.Text)
    number=db.Column(db.Integer)
    
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
    