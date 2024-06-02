import os
import smtplib
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
smtp_port = 465
smtp_user = os.getenv('MAIL_USERNAME')
smtp_password = os.getenv('MAIL_PASSWORD')

sender_email = smtp_user
receiver_email = 'jrepoylo143@gmail.com'
message = MIMEText('Test email body')
message['Subject'] = 'Test Email'
message['From'] = sender_email
message['To'] = receiver_email

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_user, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print('Email sent successfully')
except Exception as e:
    print(f'Failed to send email: {e}')
