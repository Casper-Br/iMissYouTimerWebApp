from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__, static_folder='static', static_url_path='')

# SQLite database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timer.db'
# USE THIS WHEN DEPLOYING app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Timer model
class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration_seconds = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=True)

# Create the table (only need to run once, only runs if there is no db yet)
with app.app_context():
    db.create_all()

@app.route('/submit-time', methods=['POST'])
def submit_time():
    try:
        data = request.json
        days = int(data.get('days', 0))
        hours = int(data.get('hours', 0))
        minutes = int(data.get('minutes', 0))
        seconds = int(data.get('seconds', 0))
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid input: all time values must be integers.'}), 400

    # Prevent negative inputs
    if any(x < 0 for x in [days, hours, minutes, seconds]):
        return jsonify({'status': 'error', 'message': 'Negative values are not allowed.'}), 400

    duration = days * 86400 + hours * 3600 + minutes * 60 + seconds

    # Prevents duration of zero
    if duration <= 0:
        return jsonify({'status': 'error', 'message': 'Duration must be greater than zero.'}), 400
    
    now = datetime.now(timezone.utc)

    timer = Timer.query.first()
    if not timer:
        timer = Timer(duration_seconds=duration, start_time=now)
        db.session.add(timer)
    else:
        timer.duration_seconds = duration
        timer.start_time = now

    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/get-remaining-time', methods=['GET'])
def get_remaining_time():
    timer = Timer.query.first()
    if not timer or timer.start_time is None:
        return jsonify({'remaining_seconds': 0})
    # Ensure start_time is timezone-aware (because sqlite removes timezone aware state)
    start_time = timer.start_time
    # Force Timezone awareness (assume it's in UTC (works because time is set to UTC before saving)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
    remaining = timer.duration_seconds - elapsed
    if remaining < 0:
        remaining = 0

    return jsonify({'remaining_seconds': int(remaining)})

@app.route('/')
def index():
    return app.send_static_file('index.html')