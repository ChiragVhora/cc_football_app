from website import create_app
from flask import session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import pandas as pd

app = create_app()

socketio = SocketIO(app)



##################################### Game Portion #####################################

# Game Portion ----------------------------------
# df = pd.read_csv(r"C:\Users\chira\Documents\1 LOYALIST\Term 2\2006\CodeKikkers\DATA\W13-deployment.csv")
df = pd.read_csv(r"W13-deployment.csv")
df.columns
# player data which will populate dropdowns in game 
players = {
    "goalkeepers": list(df[df['Goalkeeper']==1]['Player_Name']),    # filtering Gk names
    "defenders": list(df[df['Defender']==1]['Player_Name']),
    "attackers": list(df[df['Attaking_Midfielder']==1]['Player_Name'])
}

# Keep track of selected players
selected_players = {
    "goalkeeper": None,
    "defenders": [],
    "attackers": []
}

# leader board list
Leader_board_uids = []

# Dictionary to store the selected players by each user
selected_players_by_user = {}


active_user = 0

@socketio.on('connect')
def handle_connect():
    global active_user
    # Handle new WebSocket connection
    # Assign a unique ID to the connected user
    user_id = request.sid
    # Store the connected user in the session
    
    print(user_id, "connected-connect called ! #connhere")

    selected_players_by_user[user_id] = None
    # first just created
    active_user += 1
    # Add the user to the list of connected users
    session['connected_users'] = session.get('connected_users', set())
    session['connected_users'].add(user_id)
    print("connected user session : ", session['connected_users'])
    # Emit an event to the client to acknowledge the connection
    emit('connected', {'user_id': user_id})
    emit('user_count', {'count': active_user}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    global active_user
    # Handle WebSocket disconnection
    # Get the user ID of the disconnected user
    active_user -= 1

    # Assign a unique ID to the connected user
    user_id = request.sid

    print(user_id, "disconnected !")

    del selected_players_by_user[user_id]

    user_id = session.get('user_id')
    # Remove the user from the list of connected users
    session['connected_users'].discard(user_id)
    emit('user_count', {'count': active_user}, broadcast=True)


# @socketio.on('player_selection')
# def handle_player_selection(data):
#     print("player_selection called! @herePS")
#     # Process player selection data from the client
#     selected_player = data['selected_player']
#     # Get the user ID of the current user
#     user_id = session.get('user_id')
#     # Store the selected player in the dictionary of selected players by user

#     user_id = request.sid
#     selected_players_by_user[user_id] = selected_player
    
#     print()
#     print(len(selected_players_by_user) , (selected_players_by_user))
#     print()
#     # Check if all players have made their selections
#     flag = len(selected_players_by_user) == active_user and len(selected_players_by_user)>3
#     print(flag)
#     if flag:
#         # Determine the winner based on player ratings
#         winner = max(selected_players_by_user.values(), key=lambda x: players_ratings[x])
#         session['winner'] = winner
#         # Emit an event to the client to announce the winner
#         emit('winner_announcement', {'winner': winner}, broadcast=True)

#         # update leader boards 
#         Leader_board_uids.append(user_id)
#         # Emit an event to the client to announce the winner
#         emit('leader_board_update_announced', {'leader_list': Leader_board_uids}, broadcast=True)


#         selected_players_by_user.clear()


@socketio.on('player_selection_list')   # when user selects player for winning.
def handle_player_selection(data):
    print("player_selection called! @herePS")
    # Process player selection data from the client
    selected_playerlist = data['selected_player_list']
    # Get the user ID of the current user
    user_id = session.get('user_id')
    # Store the selected player in the dictionary of selected players by user

    user_id = request.sid
    selected_players_by_user[user_id] = selected_playerlist
    
    print()
    print(len(selected_players_by_user) , (selected_players_by_user))
    print()
    # Check if all players have made their selections
    flag = len(selected_players_by_user) == active_user and len(selected_players_by_user)>1
    print(flag)
    if flag:
        # Determine the winner based on player ratings
        winner_user_id = user_id  # user with higher ratings combined
        max_score = 0
        users_score_dict = {}
        for uid,items in selected_players_by_user.items():
            print(uid,items)
            s_l = [get_rating(name) for name in items]
            score_ = sum(s_l)
            print(uid,score_)
            if score_ > max_score:
                max_score = score_
                winner_user_id = uid
            users_score_dict[uid] = score_        
            print(users_score_dict)


        # winner = max(selected_players_by_user.values(), key=lambda x: players_ratings[x])
        # session['winner'] = winner
        session['winner'] = winner_user_id

        
        # Emit an event to the client to announce the winner
        emit('winner_announcement', {'winner': winner_user_id, 'winner_players': selected_players_by_user[winner_user_id], 'score':max_score}, broadcast=True)

        # update leader boards 
        Leader_board_uids.append(f"{winner_user_id}")
        # Emit an event to the client to announce the winner
        emit('leader_board_update_announced', {'leader_list': Leader_board_uids}, broadcast=True)

        selected_players_by_user.clear()

def get_rating(player_name):
    # getting rating of the player
    try:
        list_ = list(df[df['Player_Name']==player_name]['Rating'])
        print(sum(list_)/len(list_))
        return sum(list_)/len(list_)
    except:
        return 0





####################################################################################################

if __name__ == '__main__':
    # socketio.run(app, debug=True, host="0.0.0.0",port=8080)
    socketio.run(app, debug=True,port=8080)


