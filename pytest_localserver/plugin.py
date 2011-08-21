# Copyright (C) 2011 Sebastian Rahlf <basti at redtoad dot de>
#
# This program is release under the MIT license. You can find the full text of
# the license in the LICENSE file.

from pytest_localserver import http, https, smtp

def pytest_funcarg__httpserver(request):
    """The returned ``httpserver`` provides a threaded HTTP server instance
    running on a randomly assigned port on localhost. It can be taught which
    content (i.e. string) to serve with which response code and comes with
    following attributes:

    * ``code`` - HTTP response code (int)
    * ``content`` - content of next response (str)
    * ``headers`` - response headers (dict)

    Once these attribute are set, all subsequent requests will be answered with
    these values until they are changed or the server is stopped. A more
    convenient way to change these is ::

        httpserver.serve_content(content=None, code=200, headers=None) 

    The server address can be found in property
                                            
    * ``url``
                                                
    which is the string representation of tuple ``server_address`` (host as
    str, port as int).
    
    Example::
        
        def test_retrieve_some_content(httpserver):
            httpserver.serve_content(open('cached-content.xml').read())
            assert my_content_retrieval(httpserver.url) == 'Found it!'

    """
    server = http.Server()
    server.start()
    request.addfinalizer(server.stop)
    return server

def pytest_funcarg__httpsserver(request):
    """The returned ``httpsserver`` (note the additions S!) provides a threaded
    HTTP server instance similar to funcarg ``httpserver`` but with SSL
    encryption.
    """
    server = https.Server()
    server.start()
    request.addfinalizer(server.stop)
    return server

def pytest_funcarg__smtpserver(request):
    """The returned ``smtpserver`` provides a threaded instance of
    ``smtpd.SMTPServer`` runnning on localhost.  It has the following
    attributes:

    * ``addr`` - server address as tuple (host as str, port as int)
    """
    server = smtp.Server()
    server.start()
    request.addfinalizer(server.stop)
    return server