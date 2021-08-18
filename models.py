from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """
    User model should contain:
    Data:
    --> Favorite team
    --> Username
    --> Email
    --> Password
    --> Name
    --> Bio
    --> Picture
    Methods:
    --> Register
    --> Authenticate
    """
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.Text, nullable=False, unique=True)
    
    password = db.Column(db.Text, nullable=False)
    
    email = db.Column(db.Text, nullable=False, unique=True)

    first_name = db.Column(db.Text, nullable=False)
    
    @classmethod
    def register(cls, username, password):
        """Register user with hashed password and return user"""
        
        # hash password with bcrpyt
        hashed = bcrypt.generate_password_hash(password)
        
        # turn bytestring into utf8 string
        hashed_utf8 = hashed.decode("utf8")
        
        # return instance of user w/ username and hashed password
        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        """ Validate that user exists & password is correct. If valid, return user. Else, return false """
        
        # check if username exists in database
        username_auth = User.query.filter_by(username=username).first()
        
        # if the username is in the table AND bcrypt returns the same hash for the password stored in the user table and password from form, return authorized user instance
        if username_auth and bcrypt.check_password_hash(username_auth.password, password):
            # return user instance
            return username_auth
        else:
            # if username is not in db or password does not match, deny
            return False
    
    
    
class Team(db.Model):
    """
    
    """