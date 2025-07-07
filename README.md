# Flask Chat App
A real-time chat app built with Flask and Flask-SocketIO.

## Setup
Use the following to run the site locally.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo docker build -t flask-docker .
sudo docker run --network host flask-docker
```

## Deployment
Deploy on Render. Commits to main will be automatically deployed.
