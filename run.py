import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
app.debug = FLASK_DEBUG

GMAIL_APP_USER = os.getenv("GMAIL_APP_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            return render_template('index.html', 
                                   error="All fields are required.",
                                   name=name, email=email, message=message,
                                   submitted=False)

        msg = EmailMessage()
        msg['Subject'] = f"Rising Hammer Contact from {name}"
        msg['From'] = GMAIL_APP_USER
        msg['To'] = GMAIL_APP_USER
        msg.set_content(f"From: {name} <{email}>\n\n{message}")
        msg['Reply-To'] = email

        try:
            if app.debug:
                print("---- DEBUG EMAIL MODE ----", flush=True)
                print(msg, flush=True)
                print("--------------------------", flush=True)
            else:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(GMAIL_APP_USER, GMAIL_APP_PASSWORD)
                    smtp.send_message(msg)

            return redirect(url_for('thankyou'))

        except Exception as e:
            return render_template('index.html',
                                   error="Failed to send email. Please try again later.",
                                   name=name, email=email, message=message,
                                   submitted=False)

    # GET request
    return render_template('index.html', submitted=False)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=FLASK_DEBUG)
