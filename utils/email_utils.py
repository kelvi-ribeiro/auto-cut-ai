import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email_Config, subject, msgBody):    
    email_no_reply = email_Config['email_no_reply']
    email_to = email_Config['email_to']
    password = email_Config['password']
    message = MIMEMultipart()
    message['From'] = email_no_reply
    message['To'] = email_to
    message['Subject'] = subject

    message.attach(MIMEText(msgBody, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(email_no_reply, password)
        server.sendmail(email_no_reply, email_to, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")