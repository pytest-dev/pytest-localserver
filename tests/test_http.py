import StringIO
import urllib2

from pytest_localserver import http

def test_httpserver_funcarg(httpserver):
    assert isinstance(httpserver, http.Server)
    assert httpserver.is_alive()
    assert httpserver.server_address

def test_server_does_not_serve_file_at_startup(httpserver):
    assert httpserver.code == 204
    assert httpserver.file is None

def test_server_is_killed(httpserver):
    httpserver.stop()
    assert not httpserver.is_alive()

#def test_simple_GET_request(httpserver):
#    httpserver.serve_file(StringIO.StringIO('TEST!'))
#    content = urllib2.urlopen(httpserver.url).read()
#    assert False