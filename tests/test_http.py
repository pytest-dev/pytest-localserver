import StringIO
import urllib2

from pytest_localserver import http, plugin

def pytest_funcarg__httpserver(request):
    # define funcargs here again in order to run tests without having to 
    # install the plugin anew every single time
    return plugin.pytest_funcarg__httpserver(request)

def test_httpserver_funcarg(httpserver):
    assert isinstance(httpserver, http.Server)
    assert httpserver.is_alive()
    assert httpserver.server_address

def test_server_does_not_serve_file_at_startup(httpserver):
    assert httpserver.code == 204
    assert httpserver.content is None

def test_server_is_killed(httpserver):
    assert httpserver.is_alive()
    httpserver.stop()
    assert not httpserver.is_alive()

def test_some_content_retrieval(httpserver):
    httpserver.serve_content('TEST!')
    resp = urllib2.urlopen(httpserver.url)
    assert resp.read() == 'TEST!'
    assert resp.code == 200

def test_GET_request(httpserver):
    httpserver.serve_content('TEST!', headers={'Content-type': 'text/plain'})
    req = urllib2.Request(httpserver.url)
    req.add_header('User-Agent', 'Test method')
    req.add_header('Accept-encoding', 'gzip')
    resp = urllib2.urlopen(req)
    assert resp.read() == 'TEST!'
    assert resp.code == 200
    assert resp.headers.getheader('Content-type') == 'text/plain'

