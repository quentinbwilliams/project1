from app.config import app
from flask import render_template
from models.team import Team
from models.player import Player

@app.route("/team/<int:team_id>", methods=["GET"])
def show_team_data(team_id):
    """ Serves info on current team """
    team = Team.query.filter_by(id=f"{team_id}").first()
    players = Player.query.filter_by(team_id=f"{team_id}").all()
    return render_template('team_home.html',team=team, players=players)