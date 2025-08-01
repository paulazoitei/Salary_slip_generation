import smtplib
from email.message import EmailMessage
import mimetypes
import os
from dotenv import load_dotenv

class EmailService:
    @staticmethod
    def sendemail(to, subject, body, attachments=[]):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = "azoiteipaul2003@gmail.com"
        msg['To'] = to
        msg.set_content(body)
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")

        for filepath in attachments:
            if not os.path.isfile(filepath):
                continue
            mime_type, _ = mimetypes.guess_type(filepath)
            mime_type, mime_subtype = mime_type.split('/') if mime_type else ('application', 'octet-stream')

            with open(filepath, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype=mime_type,
                    subtype=mime_subtype,
                    filename=os.path.basename(filepath)
                )

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_user,email_pass)
                server.send_message(msg)
        except Exception as e:
            print(f"[ERROR] Failed to send email to {to}: {e}")
