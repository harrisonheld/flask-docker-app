## Setup
Copy .env.example to .env, and fill in the variables.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo docker build -t flask-docker .
sudo docker run -p 5000:5000 flask-docker
```

## Deployment
Deploy on Render. Commits to main will be automatically deployed.
