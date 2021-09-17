from app.config import app
from app.user import login
from flask import Flask, render_template, redirect, session
from forms import RegistrationForm, LoginForm
from models.join_tables import db, connect_db, UserLeague, UserTeam
from models.league import League, season
from models.team import Team
from models.player import Player
from models.user import User
from models.match import Match
from api.api_client import api_football
from werkzeug.exceptions import Unauthorized

@app.route("/", methods=["GET"])
def homepage():
    login()

@app.route("/feed")
def show_feed():
    if "username" not in session:
        return redirect("/login")
    else:
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        return render_template("feed.html", user=user)

@app.route("/league/<int:league_id>", methods=["GET"])
def league_page(league_id):
    """ Show Standings """
    league = League.query.filter_by(id=f"{league_id}").first()
    teams = Team.query.filter_by(league_id=f"{league_id}").all()
    return render_template('league_home.html', league=league, teams=teams)

@app.route("/team/<int:team_id>", methods=["GET"])
def show_team_data(team_id):
    """ Serves info on current team """
    team = Team.query.filter_by(id=f"{team_id}").first()
    players = Player.query.filter_by(team_id=f"{team_id}").all()
    return render_template('team_home.html',team=team, players=players)


@app.route("/players/<int:player_id>", methods=["GET"])    
def show_player_data(player_id):
    player = Player.query.filter_by(id=f"{player_id}")
    return render_template("player.html",player=player)
    
@app.route("/players/compare/<int:player1_id>/<int:player2_id>")
def compare_players(player1_id,player2_id):
    player1 = Player.query.filter_by(id=f"{player1_id}")
    player2 = Player.query.filter_by(id=f"{player2_id}")
    return render_template("player_comparison.html", player1=player1,player2=player2)
    