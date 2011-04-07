# Copyright (C) 2010-2011 Sebastian Rahlf <basti at redtoad dot de>
#
# This program is release under the BSD License. You can find the full text of
# the license in the LICENSE file.

import BaseHTTPServer
import sys
import threading

class Server (BaseHTTPServer.HTTPServer, threading.Thread):

    """
    Small test server which can be taught which files to serve with which 
    response code. Try the following snippet for testing API calls::
        
        server = TestServer(port=8080)
        server.start()
        print 'Test server running at http://%s:%i' % server.server_address
        server.serve_file(code=503)
        # any call to http://localhost:8080 will get a 503 response.
        # ...
        
    """

    def __init__(self, host='localhost', port=0, threadname=None):
        BaseHTTPServer.HTTPServer.__init__(self, (host, port), RequestHandler)

        # Workaround for Python 2.4: using port 0 will bind a free port to the 
        # underlying socket. The server_address, however, is not reflecting 
        # this! So we need to adjust it manually.
        if self.server_address[1] == 0: 
            self.server_address = (self.server_address[0], self.server_port)

        self.content, self.code = (None, 204) # HTTP 204: No Content
        self.logging = False

        # initialise thread
        self.threadname = threadname or self.__class__
        threading.Thread.__init__(self, name=self.threadname)
    
    def __repr__(self):
        return '<http.Server %s:%s>' % self.server_address

    @property
    def url(self):
        if self.server_port == 80:
            return 'http://%s' % self.server_name
        return 'http://%s:%s' % self.server_address

    def run(self):
        self.serve_forever()

    def stop(self, timeout=None):
        """
        Stops test server.
        """
        self.shutdown()
        self.join(timeout)

    def serve_content(self, content, code=200):
        """
        Serves string content (with specified HTTP error code) as response to
        all subsequent request.
        """
        self.content, self.code = (content, code)


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    """
    Handler for HTTP requests serving files specified by server instance.
    """
    
    def log_message(self, format, *args):
        """
        Overrides standard logging method.
        """
        if self.server.logging:
            sys.stdout.write("%s - - [%s] %s\n" % (self.address_string(), 
                self.log_date_time_string(), format % args))
        
    def do_GET(self):
        """
        Any GET response will be sent ``self.server.file`` as message and 
        ``self.server.code`` as response code.
        """
        self.send_response(self.server.code)
        self.end_headers()
        self.wfile.write(self.server.content)
        return


if __name__ == '__main__':
    import time

    server = Server()
    server.start()
    server.logging = True
    
    print 'HTTP server is running at http://%s:%i' % (server.server_address)
    print 'Type <Ctrl-C> to stop'
    
    server.serve_content(open(__file__).read(), 302)
    
    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        print '\rstopping...'
    server.stop()
    
