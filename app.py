from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import random, string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Models
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    is_system = db.Column(db.Boolean, default=False)  # Flag for system messages

# Initialize the DB on startup
with app.app_context():
    db.create_all()

user_data = {}  # maps session IDs to name/color

def random_name():
    return "Guest" + ''.join(random.choices(string.digits, k=3))

def random_color():
    return "#" + ''.join(random.choices('0123456789ABCDEF', k=6))

def get_active_users():
    return [{"name": user["name"], "color": user["color"]} for user in user_data.values()]

def send_message(msg, name, color, is_system=False):
    # Save the message to DB
    db.session.add(ChatMessage(name=name, color=color, msg=msg, is_system=is_system))
    db.session.commit()

    # Emit the message to all users
    emit("message", {
        "msg": msg,
        "name": name,
        "color": color,
        "is_system": is_system
    }, broadcast=True)

def send_system_message(msg):
    # Find the current system message
    send_message(msg, "System", "#888", is_system=True)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    sid = request.sid
    name = random_name()
    color = random_color()
    user_data[sid] = {"name": name, "color": color}

    # Send the user their initial data
    emit("user_init", {"name": name, "color": color})

    # Send all past messages, including system messages
    past_messages = ChatMessage.query.all()
    for msg in past_messages:
        emit("message", {
            "msg": msg.msg,
            "name": msg.name,
            "color": msg.color
        })
    
    send_system_message(f"{name} joined the chat.")

    # Notify all users of the updated user list
    emit("user_list", get_active_users(), broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    user = user_data.pop(sid, None)
    if user:
        send_system_message(f"{user['name']} left.")
        emit("user_list", get_active_users(), broadcast=True)

@socketio.on("chat")
def on_chat(data):
    sid = request.sid
    user = user_data.get(sid, {"name": "??", "color": "#000"})
    msg = data["msg"]

    # Send the regular chat message
    send_message(msg, user["name"], user["color"])

@socketio.on("name_change")
def on_name_change(data):
    sid = request.sid
    new_name = data["name"].strip()
    if new_name:
        old_name = user_data[sid]["name"]
        user_data[sid]["name"] = new_name
        system_msg = f"{old_name} changed name to {new_name}"
        send_system_message(system_msg)
        emit("user_list", get_active_users(), broadcast=True)

@socketio.on("get_users")
def on_get_users():
    emit("user_list", get_active_users())

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
