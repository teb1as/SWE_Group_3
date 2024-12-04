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

# Spotify API credentials
SPOTIPY_CLIENT_ID = '5cf10df01f7e497a8bd1567dff8e7a6a'
SPOTIPY_CLIENT_SECRET = '5aaf5b8eda6b44a79a4c6c64b735ba29'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-library-read playlist-modify-public user-read-playback-state user-modify-playback-state playlist-read-private'

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
)

# Initialize database
db = SQLAlchemy(app)

# User Dashboard Model
class UserDashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    user_name = session.get('user_name')
    sp_user_name = session.get('sp_user_name')
    return render_template('index.html', user_name=user_name, sp_user_name = sp_user_name)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = UserDashboard.query.filter_by(username=username).first()
    
    if user and user.password == password:
        session['user_name'] = username
        return redirect(url_for('home'))
    
    return "Invalid username or password", 400

@app.route('/create_dashboard', methods=['POST'])
def create_dashboard():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if UserDashboard.query.filter_by(username=username).first():
        return "Username already exists", 400
        
    new_user = UserDashboard(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    session['user_name'] = username
    return redirect(url_for('home'))

@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form.get('username')
    new_password = request.form.get('new_password')
    
    user = UserDashboard.query.filter_by(username=username).first()
    if user:
        user.password = new_password
        db.session.commit()
        return redirect(url_for('home'))
    
    return "User not found", 400

@app.route('/spotify_login')
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization code not found", 400

    try:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info

        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        session['sp_user_name'] = user_info.get('display_name', 'User')  # if no username, just display user

        print("Session after login:", session)
    except Exception as e:
        print("Error during callback:", e)
        return "Failed to get access token", 500

    return redirect(url_for('home'))

    # code = request.args.get('code')
    # token_info = sp_oauth.get_access_token(code)
    # session['token_info'] = token_info
    # return redirect(url_for('home'))

@app.route('/get_playlists', methods=['GET'])
def get_playlists():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))  # redirect to login

    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists(limit=10)  # fetch playlists (max 10)
    newplaylists = [x for x in playlists['items'] if x is not None]
    playlist_data = [
        {'name': playlist['name'], 'url': playlist['external_urls']['spotify'], 'uri' : playlist['uri']}
        for playlist in newplaylists
    ]

    return jsonify(playlist_data)

@app.route('/play_music', methods=['POST'])
def play_music():
    data = request.json
    uri = data.get('uri')
    token_info = session.get('token_info', None)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.start_playback(device_id=None, context_uri=uri, uris=None, offset= {'position': 0}, position_ms=0)

    return jsonify({"message": "Music playback has begun"})


@app.route('/pause_music', methods=['POST'])
def pause_music():
    token_info = session.get('token_info', None)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.pause_playback()

    return jsonify({"message": "Music paused"})


@app.route('/resume_music', methods=['POST'])
def resume_music():
    token_info = session.get('token_info', None)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.start_playback()

    return jsonify({"message": "Music resumed"})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

