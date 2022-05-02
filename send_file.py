

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "email"
toaddr = "email"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Web scrapping - ANNONCE.CZ BYTY"
body = "Tabulka prodávaných bytů v ČŘ"
msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
filename = "annonce_byty.xlsx"
attachment = open("annonce_byty.xlsx", "rb")

# instance of MIMEBase and named as p
file = MIMEBase('application', 'octet-stream')
file.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(file)
file.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(file)

# creates SMTP session
smt_gmail = smtplib.SMTP('smtp.gmail.com', 587)
smt_gmail.starttls()
smt_gmail.login(fromaddr, "password")
text = msg.as_string()
smt_gmail.sendmail(fromaddr, toaddr, text)
smt_gmail.quit()
