import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from dotenv import dotenv_values

def send_email(test_number, service_order, date, delegate, model, parking_slot):

    file_name = f'Reporte_No_{test_number}_Orden_{service_order}.pdf'

    credentials = dotenv_values("src/tests/.env")

    smtp_server = credentials["SERVER"]
    smtp_port = credentials["PORT"]

    smtp_username = credentials["EMAIL"]
    smtp_password = credentials["PASSWORD"]

    from_email = 'hidrolavadorasmar@hotmail.com'
    # to_email = 'hidrolavadorasmar2013@gmail.com'
    to_email = 'jujuanncho@gmail.com'
    subject = f'{file_name} del día {date}' 

    body = f"""A continuación se adjunta el reporte generado el día {date}, el cuál comprende los siguientes datos:
    * Orden del servicio: {service_order}
    * Encargado del proceso: {delegate}
    * Modelo de la bomba: {model}
    * Parqueadero asignado: {parking_slot}""" 

    # message = f'Subject: {subject}\n\n{body}'


    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body))


    with open(f'data/report/{file_name}', 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name) 
        msg.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)