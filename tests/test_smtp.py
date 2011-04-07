
import smtplib
from email.mime.text import MIMEText
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

def test_init_smtpserver(tmpdir):
    missing = tmpdir.mkdir('exists')
    assert missing.check(dir=True, exists=True)
    server = smtp.Server(rootdir=missing.strpath)
    assert len(server.outbox) == 0

def test_init_smtpserver_with_missing_rootdir_fails(tmpdir):
    missing = tmpdir.join('missing')
    assert not missing.check(dir=True, exists=True)
    pytest.raises(AssertionError, smtp.Server, rootdir=missing.strpath)

def test_send_email(smtpserver):
    assert len(smtpserver.outbox) == 0
    # one mail is being sent
    send_plain_email('alice@example.com', 'webmaster@example.com',
        'Your e-mail is getting there', 'Seems like this test actually works!',
        smtpserver.addr)
    # one mail is being sent
    assert len(smtpserver.outbox) == 1
    send_plain_email('bob@example.com', 'webmaster@example.com',
        'His e-mail too', 'Seems like this test actually works!', 
        smtpserver.addr)
    # two mails are now in outbox
    assert len(smtpserver.outbox) == 2

