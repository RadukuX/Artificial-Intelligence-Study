from flaskai import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


subscriptions = db.Table('subscriptions',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
                         )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Integer, default=0)
    subs = db.relationship('Team', secondary=subscriptions, backref=db.backref('subs', lazy='dynamic'))

    def __repr__(self):
        return 'User:{' % self.username % ',' % self.email % ',' % self.admin % ',' % self.subs % '}'


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    results = db.relationship('Results', backref='team', lazy=True)
    extra = db.relationship('ExtraData', backref='team', lazy=True)

    def __repr__(self):
        return 'Team:{' % self.name % '}'


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now().date())
    time = db.Column(db.DateTime, nullable=False, default=datetime.now().time())
    opponent = db.Column(db.String(50), nullable=False)
    score = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(5), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return 'Results:{' % self.date % ',' % self.time % ',' % self.oponent % ',' % self.score % ',' % self.result % \
               ',' % self.team_id % '} '


class ExtraData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(20), nullable=False)
    investment = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    draws = db.Column(db.Integer, nullable=False)
    defeats = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    place = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return 'Extra Data: {' % self.year % ',' % self.investment % ',' % self.age % ',' % self.wins % ',' \
               % self.draws % ',' % self.defeats % ',' % self.goals % ',' % self.place % '}'
