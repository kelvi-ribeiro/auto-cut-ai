import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email_no_reply, email_to, password_no_reply, subject, msgBody):    
    message = MIMEMultipart()
    message['From'] = email_no_reply
    message['To'] = email_to
    message['Subject'] = subject

    message.attach(MIMEText(msgBody, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(email_no_reply, password_no_reply)
        server.sendmail(email_no_reply, email_to, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")