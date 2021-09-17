from app.config import app
from models.league import League
from models.team import Team
from flask import render_template, session

@app.route("/league/<int:league_id>", methods=["GET"])
def league_page(league_id):
    """ Show Standings """
    league = League.query.filter_by(id=f"{league_id}").first()
    teams = Team.query.filter_by(league_id=f"{league_id}").all()
    return render_template('league_home.html', league=league, teams=teams)