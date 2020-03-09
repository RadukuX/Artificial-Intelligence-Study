from flask_wtf import FlaskForm
from wtforms import StringField


class HomeForm(FlaskForm):
    field = StringField()