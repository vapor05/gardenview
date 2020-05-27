import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 587
smtp_server = "smtp.gmail.com"
password = os.environment["EMAIL_PASS"]
sender = os.environment["EMAIL_ACCOUNT"]
receiver = "gardenviewupdates@gmail.com"

subject = "Sending attached video"
body = "See the attached mp4 file for video from the raspberrypi."

message = MIMEMultipart()
message["From"] = sender
message["To"] = receiver
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

filename = "/Users/NicholasBocchini/Development/gardenview/01-20200527165618.mov"

with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename={filename}",
)

message.attach(part)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())
