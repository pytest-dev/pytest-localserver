# with some ideas from http://code.activestate.com/recipes/440690/
# SmtpMailsink Copyright 2005 Aviarc Corporation
# Written by Adam Feuer, Matt Branthwaite, and Troy Frever
# Licensed under the PSF License

import asyncore
import email
from mailbox import Maildir
import smtpd
import threading
import os

class Server (smtpd.SMTPServer, threading.Thread):

    WAIT_BETWEEN_CHECKS = 0.001

    def __init__(self, host='localhost', port=0, rootdir=None):
        smtpd.SMTPServer.__init__(self, (host, port), None)
        if self._localaddr[1] == 0:
            self.addr = self.getsockname()
        self.mailroot = rootdir
        self.maildirs = {}

        # initialise thread
        self._stopevent = threading.Event()
        self.threadName = self.__class__.__name__
        threading.Thread.__init__(self, name=self.threadName)

    def process_message(self, peer, mailfrom, rcpttos, data):
        import sys
        sys.stderr.write('process_message(%r, %r, %r, %r)\n' % (peer, mailfrom, rcpttos, data))
        msg = email.message_from_string(data)
        for recp in rcpttos:
            if not recp.lower() in self.maildirs:
                self.maildirs[recp.lower()] = Maildir(
                    os.path.join(self.mailroot, recp.lower()), None, True)
            maildir = self.maildirs[recp.lower()]
            maildir.add(msg)

    def run(self):
        while not self._stopevent.is_set():
            asyncore.loop(timeout=self.WAIT_BETWEEN_CHECKS, count=1)

    def stop(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        self.close()

    def __repr__(self):
        return '<smtp.Server %s:%s>' % self.addr

    def mailcount(self):
        print self.maildirs.values()
        return sum(len(inbox) for inbox in self.maildirs.values())

if __name__ == "__main__":
    import time
    
    server = Server()
    server.start()

    print 'SMTP server is running at %s:%i' % (server.addr)
    print 'Type <Ctrl-C> to stop'

    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        print '\rstopping...'
    finally:
        server.stop()
