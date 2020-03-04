from flask import render_template
from flaskai import app
from flaskai.forms.LoginForm import LoginForm
from flaskai.forms.RegistrationForm import RegistrationForm

posts = [
    {
        'team': 'Liverpool',
        'goals': '30'
    },

    {
        'team': 'Chelsea',
        'goals': '28'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Register', form=form)