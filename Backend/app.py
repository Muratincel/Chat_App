from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import pytz
from datetime import datetime, timezone


app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Initialize the database
with app.app_context():
    db.create_all()

FRONTEND_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

# API Endpoint to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data.get('username')
    text = data.get('text')
    
    if not username or not text:
        return jsonify({'error': 'Username and message text are required'}), 400
    
    message = Message(username=username, text=text)
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully'})

# API Endpoint to get messages
@app.route("/get_messages", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    
    # Convert UTC time to your local timezone (Example: Europe/Istanbul)
    local_tz = pytz.timezone("Europe/Bucharest")
    
    formatted_messages = []
    for msg in messages:
        utc_time = msg.timestamp.replace(tzinfo=pytz.utc)
        local_time = utc_time.astimezone(local_tz)
        formatted_messages.append({
            "username": msg.username,
            "text": msg.text,
            "timestamp": local_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(formatted_messages)

if __name__ == '__main__':
    app.run(debug=True)
