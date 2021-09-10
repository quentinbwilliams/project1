from models.join_tables import db
from models.league import season

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
    home = db.Column(db.Integer, db.ForeignKey('teams.id'))
    away = db.Column(db.Integer, db.ForeignKey('teams.id'))
    date=db.Column(db.Text)
    round = db.Column(db.Text)
    timezone=db.Column(db.Text)
    referee=db.Column(db.Text, nullable=True)
    ht_score = db.Column(db.Text,nullable=True)
    ft_score = db.Column(db.Text,nullable=True)
    et_score = db.Column(db.Text,nullable=True)
    penalty_shootout = db.Column(db.Integer,nullable=False)
    stadium_id = db.Column(db.Integer)
    stadium_name = db.Column(db.Text)
    city_name = db.Column(db.Text)
    home_goals = db.Column(db.Integer,nullable=True)
    away_goals = db.Column(db.Integer, nullable=True)
    home_win = db.Column(db.Boolean, nullable=True)
    away_win = db.Column(db.Boolean, nullable=True)
    draw = db.Column(db.Boolean, nullable=True)
    