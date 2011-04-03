
import smtplib
from email.mime.text import MIMEText

from pytest_localserver import smtp

def send_plain_email(to, from_, subject, txt, server=('localhost', 25)):
    """
    Sends a simple plain text message.
    """
    # Create a text/plain message
    msg = MIMEText(txt)
    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = ', '.join(to)

    host, port = server
    server = smtplib.SMTP(host, port)
    server.set_debuglevel(1)
    server.sendmail(from_, to, msg.as_string())
    server.quit()

def test_smtpserver_funcarg(smtpserver):
    assert isinstance(smtpserver, smtp.Server)
    assert smtpserver.is_alive()
    assert smtpserver.accepting and smtpserver.addr
    assert smtpserver.mailcount() == 0

def test_send_email(smtpserver):
    send_plain_email(
            ['alice@example.com', 'bob@example.com'], 
            'webmaster@example.com', 
            'Your e-mail is getting through', 
            'Seems like this test actually works!', 
            smtpserver.addr)
    # one mail is being sent
    assert smtpserver.mailcount() == 2
