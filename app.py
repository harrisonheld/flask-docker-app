from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random, string

app = Flask(__name__)
socketio = SocketIO(app)

user_data = {}  # maps session IDs to name/color

def random_name():
    return "Guest" + ''.join(random.choices(string.digits, k=3))

def random_color():
    return "#"+''.join(random.choices('0123456789ABCDEF', k=6))

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    sid = request.sid
    name = random_name()
    color = random_color()
    user_data[sid] = {"name": name, "color": color}
    emit("user_init", {"name": name, "color": color})
    emit("message", {"msg": f"{name} joined the chat!", "name": "System", "color": "#888"}, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    user = user_data.pop(sid, None)
    if user:
        emit("message", {"msg": f"{user['name']} left.", "name": "System", "color": "#888"}, broadcast=True)

@socketio.on("chat")
def on_chat(data):
    sid = request.sid
    user = user_data.get(sid, {"name": "??", "color": "#000"})
    emit("message", {
        "msg": data["msg"],
        "name": user["name"],
        "color": user["color"]
    }, broadcast=True)

@socketio.on("name_change")
def on_name_change(data):
    sid = request.sid
    new_name = data["name"].strip()
    if new_name:
        old_name = user_data[sid]["name"]
        user_data[sid]["name"] = new_name
        emit("message", {"msg": f"{old_name} changed name to {new_name}", "name": "System", "color": "#888"}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
