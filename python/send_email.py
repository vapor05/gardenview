import os
import email
import smtplib
import ssl
import gzip
import shutil

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 587
smtp_server = "smtp.gmail.com"
password = os.environ["EMAIL_PASS"]
sender = os.environ["EMAIL_ACCOUNT"]
receiver = "gardenviewupdates@gmail.com"
video_root = "/opt/gardenview/output"
archive_root = "/opt/gardenview/archive"

subject = "GardenView Updates!"
body = "See the attached files for video and pictures to see the motion detected by GardenView."

message = MIMEMultipart()
message["From"] = sender
message["To"] = receiver
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

dir_list = [os.path.join(video_root, f) for f in os.listdir(video_root)]
file_list = [f for f in dir_list if os.path.isfile(f)]

for file in file_list:
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment",
        filename=file
    )
    message.attach(part)

    with open(file, "rb") as f_in, gzip.open(os.path.join(archive_root, os.path.basename(file) + ".gz"), "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(file)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())
