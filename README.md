# Flask Chat App
A simple real-time multiplayer chat app built with Flask and Flask-SocketIO.

## Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker build -t flask-docker .
docker run -p 5000:5000 flask-docker