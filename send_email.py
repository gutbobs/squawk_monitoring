#!/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to,subject,body):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = "root"
        msg['To'] = to

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('<my_SMTP_server>')
        server.sendmail("root",to,msg.as_string())
        server.quit
        
if __name__ == "__main__":
	to = "<test_email_address@domain.com>"
	subject = "test email"
	body = "body\r\n"
	send_email(to,subject,body)
