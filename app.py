from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)
app.secret_key = 'a_secure_random_secret_key'  # Replace with a secure key
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# spotify api creds (from developer settings)
SPOTIPY_CLIENT_ID = '5cf10df01f7e497a8bd1567dff8e7a6a'
SPOTIPY_CLIENT_SECRET = '5aaf5b8eda6b44a79a4c6c64b735ba29'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-library-read playlist-modify-public user-read-playback-state user-modify-playback-state'

# init oauth object
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
)

# Initialize the database
db = SQLAlchemy(app)

# Database Model
class Pomodoro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    work_time = db.Column(db.Integer, nullable=False)
    break_time = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    user_name = session.get('user_name', None)
    print("User name in home route:", user_name)
    return render_template('index.html', user_name=user_name)

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # check auth code
    code = request.args.get('code')
    if not code:
        return "Authorization code not found", 400

    try:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info

        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        session['user_name'] = user_info.get('display_name', 'User')  # if no username, just display user

        print("Session after login:", session)
    except Exception as e:
        print("Error during callback:", e)
        return "Failed to get access token", 500

    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    return jsonify(user_info)

@app.route('/start_pomodoro', methods=['POST'])
def start_pomodoro():
    # check if user is authenticated
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))  # redirect to login

    # Existing logic for handling the pomodoro session
    data = request.json
    user_name = data.get('userName')
    user_email = data.get('userEmail')
    work_time = data.get('workTime', 25)
    break_time = data.get('breakTime', 5)

    # Save to database
    pomodoro = Pomodoro(user_name=user_name, user_email=user_email, work_time=work_time, break_time=break_time)
    db.session.add(pomodoro)
    db.session.commit()

    return jsonify({"message": "Pomodoro started with custom work and break times"})

@app.route('/get_playlists', methods=['GET'])
def get_playlists():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))  # redirect to login

    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists(limit=10)  # fetch playlists (max 10)
    playlist_data = [
        {'name': playlist['name'], 'url': playlist['external_urls']['spotify']}
        for playlist in playlists['items']
    ]

    return jsonify(playlist_data)

@app.route('/logout')
def logout():
    session.pop('token_info', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
