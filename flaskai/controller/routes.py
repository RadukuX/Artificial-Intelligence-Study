from flask import render_template, flash, redirect, url_for
from flaskai import app
from flaskai.forms.LoginForm import LoginForm
from flaskai.forms.RegistrationForm import RegistrationForm
from flaskai.services.user_service import UserService

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

user_service = UserService()


@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_service.register_user(form.username, form.email, form.password)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        print(form.password.data)
        print(user_service.login_user(str(form.email.data), str(form.password.data)))
        if user_service.login_user(form.email.data, form.password.data) is True:
            flash(f'Hello!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please try again!', 'danger')
    return render_template('login.html', title='Register', form=form)
