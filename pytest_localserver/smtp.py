# Copyright (C) 2011 Sebastian Rahlf <basti at redtoad dot de>
# with some ideas from http://code.activestate.com/recipes/440690/
# SmtpMailsink Copyright 2005 Aviarc Corporation
# Written by Adam Feuer, Matt Branthwaite, and Troy Frever
# which is Licensed under the PSF License

import asyncore
import email
import smtpd
import sys
import threading

class Server (smtpd.SMTPServer, threading.Thread):

    """
    Small SMTP test server. Try the following snippet for sending mail::

        server = Server(port=8080)
        server.start()
        print 'SMTP server is running on %s:%i' % server.addr

        # any e-mail sent to localhost:8080 will end up in server.outbox
        # ...

        server.stop()

    """

    WAIT_BETWEEN_CHECKS = 0.001

    def __init__(self, host='localhost', port=0):
        smtpd.SMTPServer.__init__(self, (host, port), None)
        if self._localaddr[1] == 0:
            self.addr = self.getsockname()

        self.outbox = []

        # initialise thread
        self._stopevent = threading.Event()
        self.threadName = self.__class__.__name__
        threading.Thread.__init__(self, name=self.threadName)

        # support for Python 2.4 and 2.5
        if sys.version_info[:2] < (2, 6):
            self._stopevent.is_set = self._stopevent.isSet
            self.is_alive = self.isAlive

        # support for Python 2.4
        if not hasattr(self.outbox, '__len__'):
            self.outbox.__len__ = lambda: len([msg for msg in self.outbox])

    def process_message(self, peer, mailfrom, rcpttos, data):
        """
        Adds message to outbox.
        """
        self.outbox += [email.message_from_string(data)]

    def run(self):
        """
        Threads run method.
        """
        while not self._stopevent.is_set():
            asyncore.loop(timeout=self.WAIT_BETWEEN_CHECKS, count=1)

    def stop(self, timeout=None):
        """
        Stops test server.

        :param timeout: When the timeout argument is present and not None, it
        should be a floating point number specifying a timeout for the operation
        in seconds (or fractions thereof).
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        self.close()

    def __del__(self):
        self.stop()

    def __repr__(self):
        return '<smtp.Server %s:%s>' % self.addr

if __name__ == "__main__":
    import time

    server = Server()
    server.start()

    print 'SMTP server is running on %s:%i' % server.addr
    print 'Type <Ctrl-C> to stop'

    try:

        try:
            while True:
                time.sleep(1)
        finally:
            print '\rstopping...'
            server.stop()

    except KeyboardInterrupt:
        # support for Python 2.4 dictates that try ... finally is not used
        # together with any except statements
        pass
