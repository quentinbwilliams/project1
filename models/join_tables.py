from flask_sqlalchemy import SQLAlchemy
from config import 

UserLeague = db.Table("users_leagues",
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete = "cascade")),
                      db.Column("league_id", db.Integer, db.ForeignKey("leagues.id", ondelete="cascade")))

UserTeam = db.Table("users_teams",
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete = "cascade")),
                      db.Column("team_id", db.Integer, db.ForeignKey("teams.id", ondelete="cascade")))