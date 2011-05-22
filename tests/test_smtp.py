
import smtplib
from email.MIMEText import MIMEText
import pytest

from pytest_localserver import plugin, smtp

def send_plain_email(to, from_, subject, txt, server=('localhost', 25)):
    """
    Sends a simple plain text message via SMTP.
    """
    if type(to) in (tuple, list):
        to = ', '.join(to)
    
    # Create a text/plain message
    msg = MIMEText(txt)
    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to

    host, port = server
    server = smtplib.SMTP(host, port)
    server.set_debuglevel(1)
    server.sendmail(from_, to, msg.as_string())
    server.quit()

def pytest_funcarg__smtpserver(request):
    # define funcargs here again in order to run tests without having to 
    # install the plugin anew every single time
    return plugin.pytest_funcarg__smtpserver(request)

def test_smtpserver_funcarg(smtpserver):
    assert isinstance(smtpserver, smtp.Server)
    assert smtpserver.is_alive()
    assert smtpserver.accepting and smtpserver.addr

def test_init_smtpserver():
    server = smtp.Server()
    assert len(server.outbox) == 0

def test_send_email(smtpserver):
    # outbox is empty
    assert len(smtpserver.outbox) == 0

    # send one e-mail
    send_plain_email('alice@example.com', 'webmaster@example.com',
        'Your e-mail is getting there', 'Seems like this test actually works!',
        smtpserver.addr)
    msg = smtpserver.outbox[-1]
    assert msg['To'] == 'alice@example.com'
    assert msg['From'] == 'webmaster@example.com'
    assert msg['Subject'] == 'Your e-mail is getting there'
    
    # send another e-mail
    send_plain_email('bob@example.com', 'webmaster@example.com',
        'His e-mail too', 'Seems like this test actually works!', 
        smtpserver.addr)
    
    msg = smtpserver.outbox[-1]
    assert msg['To'] == 'bob@example.com'
    assert msg['From'] == 'webmaster@example.com'
    assert msg['Subject'] == 'His e-mail too'
    
    # two mails are now in outbox
    assert len(smtpserver.outbox) == 2

