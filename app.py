from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# API route to start the Pomodoro timer
@app.route('/start_pomodoro', methods=['POST'])
def start_pomodoro():
    data = request.json
    work_time = data.get('workTime', 25)  # Default work time is 25 minutes
    break_time = data.get('breakTime', 5)  # Default break time is 5 minutes

    # Log the values to show on the server side (you can expand this to store the data)
    print(f"Work Time: {work_time} minutes, Break Time: {break_time} minutes")

    return jsonify({"message": "Pomodoro started with custom work and break times"})

if __name__ == '__main__':
    app.run(debug=True)
