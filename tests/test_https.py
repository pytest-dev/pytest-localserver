import sys

import pytest
import requests

from pytest_localserver import https, plugin


def pytest_funcarg__httpsserver(request):
    # define funcargs here again in order to run tests without having to
    # install the plugin anew every single time
    return plugin.pytest_funcarg__httpsserver(request)


def test_httpsserver_funcarg(httpsserver):
    assert isinstance(httpsserver, https.SecureContentServer)
    assert httpsserver.is_alive()
    assert httpsserver.server_address


def test_server_does_not_serve_file_at_startup(httpsserver):
    assert httpsserver.code == 204
    assert httpsserver.content is None


def test_server_is_killed(httpsserver):
    assert httpsserver.is_alive()
    httpsserver.stop()
    assert not httpsserver.is_alive()


def test_server_is_deleted(httpsserver):
    assert httpsserver.is_alive()
    httpsserver.__del__()
    assert not httpsserver.is_alive()


@pytest.mark.xfail('sys.version_info[0] == 3', reason="Does not work under Python 3 yet!")
def test_some_content_retrieval(httpsserver):
    httpsserver.serve_content('TEST!')
    resp = requests.get(httpsserver.url, verify=False)
    assert resp.text == 'TEST!'
    assert resp.status_code == 200


@pytest.mark.xfail('sys.version_info[0] == 3', reason="Does not work under Python 3 yet!")
def test_GET_request(httpsserver):
    httpsserver.serve_content('TEST!', headers={'Content-type': 'text/plain'})
    resp = requests.get(httpsserver.url, headers={'User-Agent': 'Test method'}, verify=False)
    assert resp.text == 'TEST!'
    assert resp.status_code == 200
    assert 'text/plain' in resp.headers['Content-type']


# FIXME get compression working!
# def test_gzipped_GET_request(httpserver):
#     httpserver.serve_content('TEST!', headers={'Content-type': 'text/plain'})
#     httpserver.compress = 'gzip'
#     resp = requests.get(httpserver.url, headers={
#         'User-Agent': 'Test method',
#         'Accept-encoding': 'gzip'
#     }, verify=False)
#     assert resp.text == 'TEST!'
#     assert resp.status_code == 200
#     assert resp.content_encoding == 'gzip'
#     assert resp.headers['Content-type'] == 'text/plain'
#     assert resp.headers['content-encoding'] == 'gzip'


@pytest.mark.xfail('sys.version_info[0] == 3', reason="Does not work under Python 3 yet!")
def test_HEAD_request(httpsserver):
    httpsserver.serve_content('TEST!', headers={'Content-type': 'text/plain'})
    print(httpsserver.url)
    resp = requests.head(httpsserver.url, verify=False)
    assert resp.status_code == 200
    assert resp.headers['Content-type'] == 'text/plain'
