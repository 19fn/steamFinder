import smtplib
from email.message import EmailMessage

def mailTo(msg):
    mail = EmailMessage()
    mail.set_content(f"{msg}")
    mail["Subject"] = f"{GAME} - STEAM"
    mail["From"] = "xxxxxxx@gmail.com"
    mail["To"] = "xxxxxxx@gmail.com"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("xxxxxx@gmail.com", "XXXXXX")
    server.send_message(mail)
    server.quit()