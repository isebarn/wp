import smtplib
from email.mime.text import MIMEText as text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
import os

class Email:
  user = None

  def __init__(self, user):
    self.user = user
    self.sendmail()

  def sendmail(self):
    from_address= self.user['email']

    smtp_user= self.user['email']
    smtp_password= self.user['password']

    msg = MIMEMultipart()
    msg.attach(MIMEText('See attachment', "plain"))
    msg['Subject'] = "Outdated plugins"
    msg['From'] = self.user['email']
    msg['To'] = os.environ.get("RECIPENT")

    filename = "data.json"

    with open(filename, "rb") as attachment:
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())

    encoders.encode_base64(part)
    msg.attach(part)
    text = msg.as_string()

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    server = smtplib.SMTP('mail.mgdsw.info')
    server.ehlo()
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(self.user['email'], msg['To'], msg.as_string())
    server.quit()

if __name__ == "__main__":
  email = Email({'email': os.environ.get("EMAIL"), 'password': os.environ.get("PASSWORD")})
