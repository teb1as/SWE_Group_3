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
SCOPE = 'user-library-read playlist-modify-public user-read-playback-state user-modify-playback-state'

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
    return render_template('index.html', user_name=user_name)

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
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('home'))

@app.route('/get_playlists')
def get_playlists():
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            return jsonify({"error": "Not logged into Spotify"}), 401
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        # Get study-related playlists
        results = sp.search(q='study music', type='playlist', limit=5)
        playlists = results['playlists']['items']
        
        playlist_data = [{
            'name': playlist['name'],
            'id': playlist['id'],
            'image_url': playlist['images'][0]['url'] if playlist['images'] else None
        } for playlist in playlists]
        
        return jsonify(playlist_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/play_playlist/<playlist_id>')
def play_playlist(playlist_id):
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            return jsonify({"error": "Not logged into Spotify"}), 401
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        sp.start_playback(context_uri=f'spotify:playlist:{playlist_id}')
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)