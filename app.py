from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# API route to start the Pomodoro timer
@app.route('/start_pomodoro', methods=['POST'])
def start_pomodoro():
    return jsonify({"message": "Pomodoro started"})

if __name__ == '__main__':
    app.run(debug=True)
