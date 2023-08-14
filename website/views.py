from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from . import db
import json
from flask_socketio import SocketIO, emit

views = Blueprint('views', __name__)



# View Pages for route
@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    # if request.method == 'POST': 
    #    if needed

    return render_template("homepageFinal.html", user=current_user)

@views.route('/player-prediction', methods=['GET', 'POST'], endpoint='prediction_page')
@login_required
def prediction_page():
    if request.method == 'POST':
        print("Post in predict players") 
        flash(message="Post method called in predictPlayers", category='success')

    return render_template("playerPrediction.html", user=current_user)

@views.route('/player-statistics', methods=['GET', 'POST'], endpoint='playerStats_page')
def playerStats_page():
    if request.method == 'POST':
        print("Post in player-statistics") 
        flash(message="Post method called in player-statistics", category='success')

    return render_template("playerStatsFinal.html", user=current_user)

@views.route('/game', methods=['GET', 'POST'], endpoint='game')
def prediction_page():
    if request.method == 'POST':
        print("Post in game") 
        flash(message="Post method called in game", category='success')

    return render_template("game.html", user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'], endpoint='dashboard')
@login_required
def prediction_page():
    if request.method == 'POST':
        print("Post in dashboard") 
        flash(message="Post method called in dashboard", category='success')

    return render_template("dashboard.html", user=current_user)




##################################### for Statistics #####################################
import pandas as pd

# Sample leagues and teams (replace this with your actual data)
# df = pd.read_csv(r"C:\Users\chira\Documents\1 LOYALIST\Term 2\2006\CodeKikkers\DATA\W13-deployment.csv")
df_stats = pd.read_csv(r"W13-deployment-stats.csv")

@views.route('/get_teams/<league>', methods=['GET'], endpoint='get_teams')
def get_teams(league):
    print("fetch call for ", league)
    # You can filter teams based on the selected league from your data
    # For example: filtered_teams = teams[league]
    filtered_teams =  list(df_stats[df_stats["Tournament"]==league]["Team"].unique())
    return jsonify({'teams': filtered_teams})

@views.route('/get_players_data', methods=['POST'], endpoint='get_players_data')
def get_players_data():
    data = request.get_json()
    selected_league = data.get('league')
    selected_team = data.get('team')

    filtered_players_data = df_stats[(df_stats["Tournament"]==selected_league) & (df_stats["Team"]==selected_team)].drop(['Team', 'Tournament'], axis=1)
    print(filtered_players_data.shape[0])
    # filtered_players_data["Unnamed: 0"] = range(1, filtered_players_data.shape[0]+1)
    filtered_players_data.insert(0, 'Unnamed: 0', range(1, filtered_players_data.shape[0]+1))
    # print(filtered_players_data.to_json(orient ='index'))
    # print(filtered_players_data)

    return jsonify({'players': filtered_players_data.to_json(orient ='index')})



##################################### for prediction #####################################
import joblib
import numpy as np

# model_path = r"C:\Users\chira\Documents\1 LOYALIST\Term 2\2006\Random_forest_CK(9).sav"
model_path = r"Random_forest_CK(9).sav"
model = joblib.load(model_path)

@views.route('/predict', methods=['POST'], endpoint='predict')
def predict():

    # start_time = time.perf_counter()

    # Retrieve the form field values
    # print("here 1")
    # player_name = request.form.get('player_name')
    age = int(request.form.get('age'))
    height = int(request.form.get('height'))
    weight = int(request.form.get('weight'))

    forward = request.form.get('forward')
    forward = 1 if forward.lower()=="yes" else 0
    goalkeeper = request.form.get('goalkeeper')
    goalkeeper = 1 if goalkeeper.lower()=="yes" else 0
    midfielder = request.form.get('midfielder')
    midfielder = 1 if midfielder.lower()=="yes" else 0
    attacking_midfielder = request.form.get('attacking_midfielder')
    attacking_midfielder = 1 if attacking_midfielder.lower()=="yes" else 0
    center = request.form.get('center')
    center = 1 if center.lower()=="yes" else 0
    defender = request.form.get('defender')
    defender = 1 if defender.lower()=="yes" else 0

    appearances = int(request.form.get('appearances'))
    substitute_appearances = int(request.form.get('substitute_appearances'))
    playtime = request.form.get('playtime')
    goals = request.form.get('goals')
    assists = request.form.get('assists')
    yellow_cards = request.form.get('yellow_cards')
    red_cards = request.form.get('red_cards')
    set_piece_goal = request.form.get('set_piece_goal')
    passing_percentage = int(request.form.get('passing_percentage'))
    aerials_won = request.form.get('aerials_won')
    man_of_the_matches = request.form.get('man_of_the_matches')


    # print("\nhere 2")

    # Perform validation on the form field values
    if not validate_fields(age, height, weight, appearances, substitute_appearances, passing_percentage):
        return jsonify({'success': False, 'error': 'Invalid field values'})

    # print("\nhere 3")

    # Perform the player stats prediction
    prediction = predict_stats(age, height, weight, forward, goalkeeper, midfielder, attacking_midfielder, center, defender, appearances, substitute_appearances, playtime, goals, assists, yellow_cards, red_cards, set_piece_goal, passing_percentage, aerials_won, man_of_the_matches)

    # print("\nhere 4", prediction)

    # testing
    # end_time = time.perf_counter()
    # total_time = end_time - start_time
    # predict_time_list.append(total_time)
    # print(f"Average predict function time : {sum(predict_time_list)/len(predict_time_list)} ms")
    print("\n")

    # Return the predicted stats as JSON response
    return jsonify({'success': True, 'prediction': prediction[0]})

def validate_fields(age, height, weight, appearances, substitute_appearances, passing_percentage):
    # Perform validation for each field
    if age < 0 or age > 100:
        return False
    if height < 0 or height > 400:
        return False
    if weight < 0 or weight > 200:
        return False
    if appearances < 0 or appearances > 200:
        return False
    if substitute_appearances < 0 or substitute_appearances > 100:
        return False
    if passing_percentage < 0 or passing_percentage > 100:
        return False
    return True

def predict_stats(age, height, weight, forward, goalkeeper, midfielder, attacking_midfielder, center, defender, appearances, substitute_appearances, playtime, goals, assists, yellow_cards, red_cards, set_piece_goal, passing_percentage, aerials_won, man_of_the_matches):
    # Perform the player stats prediction
    # Replace this with your own prediction logic
    X = pd.DataFrame(columns=['Age', 'Height', 'Weight', 'Forward', 'Goalkeeper',
       'Midfielder', 'Attaking_Midfielder', 'Center', 'Defender',
       'Appearances', 'Substitute(Appearances)', 'Playtime(Minutes)', 'Goals',
       'Assists', 'Yellow_Cards', 'Red_Cards', 'Set_piece_Goal',
       'Passing_Percentage', 'AerialsWon', 'Man_Of_The_Matches'])
    
    input_list = [age, height, weight, forward, goalkeeper, midfielder, attacking_midfielder, center, defender, appearances, substitute_appearances, playtime, goals, assists, yellow_cards, red_cards, set_piece_goal, passing_percentage, aerials_won, man_of_the_matches]

    X.loc[0]=[x if x else 0 for x in  input_list]
    X.fillna(0)
    # print(X)
    prediction = model.predict(X)
    # Add your prediction code here to compute the predicted stats based on the input features
    return prediction



