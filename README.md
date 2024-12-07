# ClockWork 🕒

ClockWork is a sophisticated Pomodoro Timer application integrated with Spotify, designed to enhance your study sessions with synchronized music control. Built with Flask and featuring a sleek dark-themed interface, ClockWork helps you maintain focus while enjoying your favorite study playlists.

## Features ✨

- **Dual-Mode Timer**
  - Study and break timer modes
  - Customizable durations with easy adjustment controls
  - Automatic mode switching
  - Visual countdown display

- **Spotify Integration**
  - Connect with your Spotify account
  - Browse and select your playlists
  - Full playback controls (play/pause, next/previous track)
  - Seamless music integration with your study sessions

- **User Management**
  - Personal user accounts
  - Secure session management
  - Password reset functionality

- **Modern UI**
  - Clean, dark-themed interface
  - Responsive design
  - Intuitive controls

## Installation 🚀

### Prerequisites
- Python 3.x
- pip
- Spotify Premium Account
- Spotify Developer Account

### Setup

1. Clone the repository
```bash
git clone [repository-url]
cd clockwork
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Configure Spotify API credentials
Create a `.env` file in the root directory:
```env
SPOTIPY_CLIENT_ID='your_client_id'
SPOTIPY_CLIENT_SECRET='your_client_secret'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:5000/callback'
```

4. Set up the database
```python
flask db init
flask db migrate
flask db upgrade
```

5. Run the application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Usage 📖

1. Create an account or log in
2. Connect your Spotify account
3. Select a study playlist
4. Set your desired study/break durations
5. Start your productive session!

## Dependencies 📚

```
Flask==2.3.2
Flask-SQLAlchemy
spotipy
```

## API Endpoints 🛠

### Authentication
- `POST /login` - User login
- `POST /create_dashboard` - Create new account
- `POST /reset_password` - Reset password
- `GET /logout` - Logout user

### Spotify Integration
- `GET /spotify_login` - Initialize Spotify OAuth
- `GET /callback` - Handle Spotify OAuth callback
- `GET /get_playlists` - Fetch user's playlists
- `POST /play_music` - Start playback
- `POST /pause_music` - Pause playback
- `POST /resume_music` - Resume playback
- `POST /skip_track` - Skip to next track
- `POST /back_track` - Go to previous track

## Security Notes 🔒

- Current version stores passwords as plaintext (not recommended for production)
- Implements session-based authentication
- Uses OAuth 2.0 for Spotify integration

## Development Status 🔧

This project is in active development. Known areas for improvement:
- Password hashing implementation
- Enhanced error handling
- Extended timer customization options
- Additional Spotify playback features

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

[Your License Here]
