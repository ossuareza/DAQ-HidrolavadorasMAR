import smtplib

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'youremail@gmail.com'
smtp_password = 'yourpassword'

from_email = 'youremail@gmail.com'
to_email = 'recipient@example.com'
subject = 'Hello, world!'
body = 'This is a test email.'

message = f'Subject: {subject}\n\n{body}'

with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(from_email, to_email, message)