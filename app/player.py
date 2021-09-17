from app.config import app
from flask import render_template
from models.player import Player

@app.route("/players/<int:player_id>", methods=["GET"])    
def show_player_data(player_id):
    player = Player.query.filter_by(id=f"{player_id}")
    return render_template("player.html",player=player)
    
@app.route("/players/compare/<int:player1_id>/<int:player2_id>")
def compare_players(player1_id,player2_id):
    player1 = Player.query.filter_by(id=f"{player1_id}")
    player2 = Player.query.filter_by(id=f"{player2_id}")
    return render_template("player_comparison.html", player1=player1,player2=player2)