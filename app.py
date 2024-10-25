from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    return render_template('index.html')

@app.route('/start_pomodoro', methods=['POST'])
def start_pomodoro():
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

if __name__ == '__main__':
    app.run(debug=True)
