import StringIO
import urllib2

from pytest_localserver import http

def pytest_funcarg__server(request):
    server = http.Server()
    server.start()
    request.addfinalizer(server.stop)
    return server

def test_server_does_not_serve_file_at_startup(server):
    assert server.code == 204
    assert server.content is None

def test_server_is_killed(server):
    assert server.is_alive()
    server.stop()
    assert not server.is_alive()

def test_some_content_retrieval(server):
    server.serve_content('TEST!')
    resp = urllib2.urlopen(server.url)
    assert resp.read() == 'TEST!'
    assert resp.code == 200

def test_GET_request(server):
    server.serve_content('TEST!')
    req = urllib2.Request(server.url)
    req.add_header('User-Agent', 'Test method')
    req.add_header('Accept-encoding', 'gzip')
    resp = urllib2.urlopen(req)
    assert resp.read() == 'TEST!'
    assert resp.code == 200


def test_httpserver_funcarg(httpserver):
    assert isinstance(httpserver, http.Server)
    assert httpserver.is_alive()
    assert httpserver.server_address

