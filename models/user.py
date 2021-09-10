from models.join_tables import db
from models.join_tables import UserLeague, UserTeam
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    """ MANY to MANY relationship of Users to Leagues & Users to Teams """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    leagues = db.relationship("League",        
                              secondary=UserLeague, backref = db.backref("users"))
    teams = db.relationship("Team", 
                            secondary = UserTeam,
                            backref = db.backref("users"))
    
    @classmethod
    def register(cls, username, password, email):
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
            return cls(username=username, password=hashed_utf8, email=email)
        elif username_exists:
            # Should return F but let them know why
            return 'username already exists'
        elif email_exists:
            # Should return F but let them know why
            return 'that email is already registered with an account'
        
    @classmethod
    def authenticate(cls, password, email):
        """ Validate that user exists & password is correct. If valid, return user. Else, return false """
        # check if email exists in database
        email = User.query.filter_by(email=email).first()
        if email:
            authorize = bcrypt.check_password_hash(email.password, password)
            if authorize:
                username = email.username
                return username
        else:
            # if username is not in db or password does not match, deny
            return False    