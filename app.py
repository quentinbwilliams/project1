from flask import Flask, render_template, redirect, session
from forms import RegistrationForm, LoginForm
from models import db, connect_db, User, League, Team
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///matchday_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "ynwa"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route('/')
def homepage():
    return redirect('/league/PL')

@app.route("/league/PL")
def league_page():
    """ Show Standings """
    premier_league = League.query.filter_by(name="premier_league").first()
    premier_league.get_standings(premier_league)
    standings = premier_league.standings
    matches = premier_league.get_upcoming_matches(premier_league)
    return render_template('league_home.html', standings=standings, matches=matches)

@app.route("/league/PL/teams/<int:team_id>")
def show_team_data(team_id):
    """ Serves info on current team """
    premier_league = League.query.filter_by(name="premier_league").first()
    team_info = premier_league.get_team_info(premier_league,team_id)
    print("********************", team_info)
    team_name = team_info[0]['team']['name']
    team = Team(name=team_name,id=team_id)
    db.session.add(team)
    db.session.commit()
    team_stats = team.get_team_stats(team)
    team_players=team.get_players(team)
    team_transfers=team.get_player(team)
    return render_template('team_home.html', team=team,team_stats=team_stats,team_players=team_players,team_transfers=team_transfers)


    

##################
### USER LOGIC ###
##################

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user = User.register(username, password, email)
        db.session.commit()
        session['username'] = user.username
        return redirect(f"/users/{user.username}/update")
    else:
        return render_template("register.html", form=form)

@app.route('/users/<int:user_id>/update')
def update_user():
    """ Select favorite team, Players to follow, Change Username """
    return render_template('league_home.html')

@app.route('/users/<int:user_id>/delete', methods=["GET","POST"])
def delete_user():
    """ Delete user """
    return render_template('user_delete.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logout route."""
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """  """
    # Prevent access to non-logged-in users from acessing user page via url
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.filter_by(username=f"{username}").first()
    
    return render_template("user_home.html", user=user)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")