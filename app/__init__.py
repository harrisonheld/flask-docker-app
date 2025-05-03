from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from .routes import main
    from .sockets import register_socketio_handlers

    app.register_blueprint(main)
    register_socketio_handlers(socketio)

    with app.app_context():
        db.create_all()

    return app
