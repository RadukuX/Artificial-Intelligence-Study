from flask import render_template, flash, redirect, url_for, request
from flaskai import app
from flaskai.forms.LoginForm import LoginForm
from flaskai.forms.RegistrationForm import RegistrationForm
from flaskai.services.user_service import UserService
from flask_login import login_user, current_user, logout_user, login_required

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
@login_required
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_service.register_user(form.username.data, form.email.data, form.password.data)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if user_service.login_user(form.email.data, form.password.data)[1] is True:
            user = user_service.login_user(form.email.data, form.password.data)[0]
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Hello!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please try again!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))