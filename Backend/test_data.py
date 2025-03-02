from app import app, db, Message

with app.app_context():  # This sets up the Flask app context
    messages = Message.query.all()
    if messages:
        for msg in messages:
            print(f"{msg.id}: {msg.username} - {msg.text} ({msg.timestamp})")
    else:
        print("No messages found in the database.")
