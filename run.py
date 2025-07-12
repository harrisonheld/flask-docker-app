import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
GMAIL_APP_USER = os.getenv("GMAIL_APP_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

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

            return redirect(url_for('thank_you'))
        except Exception as e:
            return f"Failed to send email: {e}", 500

    return render_template('contact.html')


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=FLASK_DEBUG)
