from functools import total_ordering
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournId = db.Column(db.Integer)
    year = db.Column(db.Integer)
    tournStatus = db.Column(db.String(1000))
    currentRound = db.Column(db.Integer)
    currentRoundStatus = db.Column(db.String(1000))
    playerId = db.Column(db.Integer)
    lastName = db.Column(db.String(1000))
    firstName = db.Column(db.String(1000))
    position = db.Column(db.String(1000))
    total = db.Column(db.Integer)
    roundId = db.Column(db.Integer)
    scoreToPar = db.Column(db.Integer)
    strokes = db.Column(db.Integer)