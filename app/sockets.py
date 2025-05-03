from flask import request
from flask_socketio import emit
from . import db
from .models import ChatMessage
from .utils import random_name, random_color

user_data = {}

def get_active_users():
    return [{"name": user["name"], "color": user["color"]} for user in user_data.values()]

def send_message(socketio, msg, name, color, is_system=False):
    db.session.add(ChatMessage(name=name, color=color, msg=msg, is_system=is_system))
    db.session.commit()
    socketio.emit("message", {
        "msg": msg,
        "name": name,
        "color": color,
        "is_system": is_system
    })

def send_system_message(socketio, msg):
    send_message(socketio, msg, "System", "#888", is_system=True)

def register_socketio_handlers(socketio):
    @socketio.on("connect")
    def on_connect():
        sid = request.sid
        name = random_name()
        color = random_color()
        user_data[sid] = {"name": name, "color": color}

        emit("user_init", {"name": name, "color": color})

        past_messages = ChatMessage.query.all()
        for msg in past_messages:
            emit("message", {
                "msg": msg.msg,
                "name": msg.name,
                "color": msg.color,
                "is_system": msg.is_system
            })

        send_system_message(socketio, f"{name} joined the chat.")
        socketio.emit("user_list", get_active_users())

    @socketio.on("disconnect")
    def on_disconnect():
        sid = request.sid
        user = user_data.pop(sid, None)
        if user:
            send_system_message(socketio, f"{user['name']} left.")
            socketio.emit("user_list", get_active_users())

    @socketio.on("chat")
    def on_chat(data):
        sid = request.sid
        user = user_data.get(sid, {"name": "??", "color": "#000"})
        msg = data.get("msg", "")
        send_message(socketio, msg, user["name"], user["color"])

    @socketio.on("name_change")
    def on_name_change(data):
        sid = request.sid
        new_name = data.get("name", "").strip()
        if new_name:
            old_name = user_data[sid]["name"]
            user_data[sid]["name"] = new_name
            send_system_message(socketio, f"{old_name} changed name to {new_name}")
            socketio.emit("user_list", get_active_users())

    @socketio.on("get_users")
    def on_get_users():
        emit("user_list", get_active_users())