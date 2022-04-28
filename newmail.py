import smtplib
server=smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("nathan40241@gmail.com", "Badgebadge29*")
msg="An Instruder was detected"
server.sendmail("nathan40241@gmail.com","nathan40241@gmail.com",msg)
server.quit()
