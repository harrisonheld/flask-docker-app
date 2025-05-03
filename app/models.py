from . import db

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    is_system = db.Column(db.Boolean, default=False)
