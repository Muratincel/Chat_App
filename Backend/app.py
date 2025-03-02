from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
import datetime
import os
import pytz # type: ignore
from datetime import datetime, timezone
from flask_socketio import SocketIO, emit # type: ignore


app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

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

@socketio.on("send_message")
def handle_message(data):
    username = data.get("username")
    text = data.get("text")

    if not username or not text:
        return

    message = Message(username=username, text=text)
    db.session.add(message)
    db.session.commit()

    local_tz = pytz.timezone("Europe/Bucharest")
    utc_time = message.timestamp.replace(tzinfo=pytz.utc)
    local_time = utc_time.astimezone(local_tz)

    # Emit the message to all connected clients
    socketio.emit("new_message", {
        "username": message.username,
        "text": message.text,
        "timestamp": local_time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/get_messages")
def get_messages():
    messages = Message.query.all()
    
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
    socketio.run(app, debug=True)
