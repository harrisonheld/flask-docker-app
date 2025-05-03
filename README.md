# Flask Chat App
A real-time chat app built with Flask and Flask-SocketIO.

## Setup
Use the following to run the site locally.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker build -t flask-docker .
docker run -p 5000:5000 flask-docker
```

## Deployment
Deploy on Render. Commits to main will be automatically deployed.
