
import smtplib
from email.message import EmailMessage
import mimetypes
import os

class EmailService:
    @staticmethod
    def sendemail(to, subject, body, attachments=[]):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = "hr@endava.com"
        msg['To'] = to
        msg.set_content(body)

        for filepath in attachments:
            if not os.path.isfile(filepath):
                continue
            mime_type, _ = mimetypes.guess_type(filepath)
            mime_type, mime_subtype = mime_type.split('/') if mime_type else ('application', 'octet-stream')

            with open(filepath, 'rb') as f:
                msg.add_attachment(f.read(), maintype=mime_type, subtype=mime_subtype, filename=os.path.basename(filepath))


        try:
            with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587,timeout=10) as server:
                server.starttls()
                server.login("5eed7e6a7561df", "a5b2b8c13f5e10")
                server.send_message(msg)
        except Exception as e:
            print(f"[ERROR] Failed to send email to {to}: {e}")
