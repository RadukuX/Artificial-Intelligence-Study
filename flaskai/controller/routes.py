from flask import render_template, flash, redirect, url_for, request
from flaskai import app, api, Resource
from flaskai.forms.LoginForm import LoginForm
from flaskai.forms.RegistrationForm import RegistrationForm
from flaskai.services.user_service import UserService
from flask_login import login_user, current_user, logout_user, login_required
from flaskai.services.linear_reg_alg_service import LinearRegService
from flaskai.services.team_service import TeamService
import json


user_service = UserService()
linear_regression_service = LinearRegService()
team_service = TeamService()


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():   
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_service.register_user(form.username.data, form.email.data, form.password.data)
        flash(f'Account created for {form.username.data}! Now choose your teams!', 'success')
        return redirect(url_for('login')) 
    return render_template('register.html', title='Register', form=form)

@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if user_service.check_subscription(current_user.email):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('pick'))
    form = LoginForm()
    if form.validate_on_submit():
        if user_service.login_user(form.email.data, form.password.data)[1] is True:
            user = user_service.login_user(form.email.data, form.password.data)[0]
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Hello!', 'success')
            if user_service.check_subscription(form.email.data):
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                return redirect(url_for('pick'))
        else:
            flash(f'Login Unsuccessful. Please try again!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/team-picking', methods=['POST'])
@login_required
def team_picking():
    result = request.data.decode('utf-8').replace("'", "\"")
    print(request)
    print(request.data)
    raw_result = result.split(":")
    teams = raw_result[-1].replace("}", "").replace("[", "").replace("]","").replace("\"","")
    team_list = teams.split(',')
    if team_list[0] == '':
        team_list.remove(team_list[0])
    if user_service.add_teams(list(team_list), current_user.email) is True:
        return 'ok'
    else:
        return 'error'

@app.route('/pick', methods=['GET'])
def pick():
    return render_template('picks.html', title='Team Picking')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/get-your-teams', methods=['GET'])
@login_required
def get_your_teams():
    team_list = user_service.get_your_teams(current_user.email)
    json_team_list = {'teams':team_list}
    return json_team_list

@app.route('/get-info/<team_name>', methods=['GET'])
@login_required
def get_info(team_name):
    return team_service.get_info(team_name)



class LinearRegressionController(Resource):

    def get(self):
        investments = request.json['investments']
        med_age = request.json['med_age']
        wins = request.json['wins']
        equals = request.json['equals']
        defeats = request.json['defeats']
        goals = request.json['goals']
        return linear_regression_service.lin_get_multiple_var(investments, med_age, wins, equals, defeats, goals)


class DrawLinearRegression(Resource):

    def get(self, variable):
        return linear_regression_service.draw_linear_regression(variable)


api.add_resource(LinearRegressionController, '/linear-regression')
api.add_resource(DrawLinearRegression, '/draw-linear-regression/<string:variable>')