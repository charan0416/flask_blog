from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
import os  # For environment variables

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sendemail/", methods=['POST'])
def sendemail():
    if request.method == "POST":
        # Collect form data
        name = request.form['name']
        subject = request.form['subject']
        email = request.form['_replyto']
        message = request.form['message']

        # Environment variables for email and password
        yourEmail = os.getenv("YOUR_EMAIL")
        yourPassword = os.getenv("YOUR_EMAIL_PASSWORD")

        # Check if environment variables are set
        if not yourEmail or not yourPassword:
            return "Email configuration is missing. Please check your environment variables."

        # Setup SMTP connection
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(yourEmail, yourPassword)

            # Compose the email
            msg = EmailMessage()
            msg.set_content(f"First Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
            msg['To'] = email
            msg['From'] = yourEmail
            msg['Subject'] = subject

            # Send the message
            server.send_message(msg)
            server.quit()

            return redirect('/')  # Redirect to homepage after success

        except Exception as e:
            print("Failed to send email:", e)
            return "There was an issue sending the email. Please try again later."

if __name__ == "__main__":
    app.run(debug=True)



