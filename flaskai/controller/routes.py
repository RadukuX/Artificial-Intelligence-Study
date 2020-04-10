from flask import render_template, flash, redirect, url_for, request, jsonify
from flaskai import app, api, Resource
from flaskai.forms.LoginForm import LoginForm
from flaskai.forms.RegistrationForm import RegistrationForm
from flaskai.services.user_service import UserService
from flask_login import login_user, current_user, logout_user, login_required
from flaskai.services.linear_reg_alg_service import LinearRegService
from flaskai.services.team_service import TeamService
import json
from flaskai.services.markov_alg_service import MarkovService
from flaskai.services.naive_bayes_service import NaiveBayesService
from flaskai.services.k_nn_alg_service import KNearestNeighbors

user_service = UserService()
linear_regression_service = LinearRegService()
team_service = TeamService()
markov_service = MarkovService()
naive_service = NaiveBayesService()
knn_service = KNearestNeighbors()


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/business-prediction')
@login_required
def business_prediction():
    return render_template('business_prediction.html')

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

@app.route('/prediction/<team_name>', methods=['GET'])
@login_required
def get_prediction_html(team_name):
    return team_service.get_team_name(team_name)

@app.route('/prediction', methods=['GET'])
@login_required
def get_prediction():
    return render_template('prediction.html', title='Predictions')

@app.route('/livesearch', methods=['POST'])
@login_required
def search_team_live():
    opponent = request.form.get('opponent') 
    team_id = request.form.get('myTeam')
    print(opponent)
    print(team_id)
    return jsonify(team_service.get_team_live(opponent, team_id))

@app.route('/livesearch-business', methods=['POST'])
@login_required
def search_team_b():
    my_team = request.form.get('myTeam')
    print(my_team)
    return jsonify(team_service.get_team_b(my_team))


# Algorithm routes

# Markov
@app.route('/markov/informations', methods=['POST'])
@login_required
def informations():
    my_team = request.form.get('team1')
    opponent_team = request.form.get('team2')
    return jsonify(markov_service.informations(my_team, opponent_team))

@app.route('/markov/probability-matrix', methods=['POST'])
@login_required
def probability_matrix():
    my_team = request.form.get('team1')
    opponent_team = request.form.get('team2')
    last_result = str(request.form.get('lastResult'))
    power = int(request.form.get('power'))
    small_matrix = markov_service.markov_alg(my_team, opponent_team, last_result, power).tolist()
    markov_dictionary = { 'result_matrix': small_matrix }
    print(markov_dictionary)
    return markov_dictionary

@app.route('/markov/matrix', methods=['POST'])
@login_required
def markov_matrix():
    my_team = request.form.get('team1')
    opponent_team = request.form.get('team2')
    print('323' + str(my_team)+"asdf")
    big_matrix = markov_service.markov_matrix(my_team, opponent_team).tolist()
    print(big_matrix)
    markov_dictionary = { 'no_training_result': big_matrix}
    print(markov_dictionary)
    return markov_dictionary




# Naive Bayes Classifier

@app.route('/bayes/calculate', methods=['POST'])
@login_required
def bayes_calculator():
    my_team = request.form.get('team1')
    opponent_team = request.form.get('team2')
    bayes_dictionary = { 'bayes': naive_service.calculate(my_team, opponent_team) }
    return bayes_dictionary





# Linear Regression Algorithm



@app.route('/knn', methods=['POST'])
@login_required
def KNN():
    investments = int(request.form.get('investments'))
    med_age = float(request.form.get('medAge'))
    wins = int(request.form.get('wins'))
    equals = int(request.form.get('equals'))
    defeats = int(request.form.get('defeats'))
    goals = int(request.form.get('goals'))
    return jsonify(knn_service.knn(investments, med_age, wins, equals, defeats, goals))

@app.route('/linear', methods=['POST'])
@login_required
def linear_regression():
    investments = int(request.form.get('investments'))
    med_age = float(request.form.get('medAge'))
    wins = int(request.form.get('wins'))
    equals = int(request.form.get('equals'))
    defeats = int(request.form.get('defeats'))
    goals = int(request.form.get('goals'))
    return linear_regression_service.lin_get_multiple_var(investments, med_age, wins, equals, defeats, goals)


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