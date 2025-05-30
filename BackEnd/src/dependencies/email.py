import smtplib
from email.mime.text import MIMEText
from src.settings import get_settings

set = get_settings()

class EmailSender:
    def __init__(self):
        self.email = set.email
        self.password = set.password

    def send_email(self, receiver, token):
        
        body = f"""
Hello!!\n
A request was made to change the password, copy the token beneath and paste it to confirm, then update the password.\n
{token}
"""
        message = MIMEText(body, 'plain')
        message['From'] = self.email
        message['To'] = receiver
        message['Subject'] = "Password Reset from App"

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, receiver, message.as_string())
            print(f"Email sent successfully to {receiver}")
        except Exception as e:
            print(f"Error sending email to {receiver}: {e}")


email = EmailSender()
