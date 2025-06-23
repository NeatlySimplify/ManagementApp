import requests

from src.settings import get_settings

setting = get_settings()

class EmailSender:
    def __init__(self):
        self.email = "ribeirodennis9@gmail.com"
        self.api = setting.mailgun

    def send_email(self, receiver, token):
        body = f"""
            Hello!!\n
            A request was made to change the password,
            copy the token beneath and paste it to confirm,
            then update the password.\n
            {receiver} \n
            {token}
        """
        to = self.email
        subject = "Password Reset from App"
        result = requests.post(
            "https://api.mailgun.net/v3/sandbox1a5be8fd70864949ab4f9683a1082c8b.mailgun.org/messages",
            auth=("api", self.api),
            data={
                "from": "Mailgun Sandbox \
                <postmaster@sandbox1a5be8fd70864949ab4f9683a1082c8b.mailgun.org>",
                "to": self.email,
                "subject": subject,
                "text": body
            }
        )
        print(result.status_code)
        return result


email = EmailSender()
