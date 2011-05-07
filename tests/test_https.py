import httplib
import StringIO
import urllib2

from pytest_localserver import http, plugin
from pytest_localserver import VERSION

def pytest_funcarg__httpsserver(request):
    # define funcargs here again in order to run tests without having to 
    # install the plugin anew every single time
    return plugin.pytest_funcarg__httpsserver(request)

def test_httpsserver_funcarg(httpsserver):
    assert isinstance(httpsserver, http.Server)
    assert httpsserver.is_alive()
    assert httpsserver.server_address

def test_server_does_not_serve_file_at_startup(httpsserver):
    assert httpsserver.code == 204
    assert httpsserver.content is None

def test_server_is_killed(httpsserver):
    assert httpsserver.is_alive()
    httpsserver.stop()
    assert not httpsserver.is_alive()

def test_some_content_retrieval(httpsserver):
    httpsserver.serve_content('TEST!')
    resp = urllib2.urlopen(httpsserver.url)
    assert resp.read() == 'TEST!'
    assert resp.code == 200

def test_GET_request(httpsserver):
    httpsserver.serve_content('TEST!', headers={'Content-type': 'text/plain'})
    req = urllib2.Request(httpsserver.url)
    req.add_header('User-Agent', 'Test method')
    req.add_header('Accept-encoding', 'gzip')
    resp = urllib2.urlopen(req)
    assert resp.read() == 'TEST!'
    assert resp.code == 200
    assert resp.headers.getheader('Content-type') == 'text/plain'
