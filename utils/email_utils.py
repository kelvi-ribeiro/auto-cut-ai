import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.notification.notification_system import NotificationSystem

notification_system = NotificationSystem()

def send_email(config, subject, msgBody):    
    use_email_notification = config["use_email_notification"]
    if not use_email_notification:
        return
    
    from_email = config["from_email"]
    from_email_password = config["from_email_password"]
    recipient_email = config["recipient_email"]
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(msgBody, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(from_email, from_email_password)
        server.sendmail(from_email, recipient_email, message.as_string())
        server.quit()
    except Exception as e:
        notification_system.notify(f"Erro no envio de e-mail: {e}")