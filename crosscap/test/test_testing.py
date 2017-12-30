"""
Tests of the testing-helpers. :-/
"""
from twisted.web.http_headers import Headers

from klein import Klein

from pytest import fixture, inlineCallbacks

from crosscap import testing


@fixture
def srv():
    class AServer(object):
        app = Klein()

        @app.route('/hello')
        def hello(self, request):
            return 123

    return testing.EZServer(AServer)


@inlineCallbacks
def test_handler(srv):
    res = yield srv.handler("hello")
    assert res == 123


def test_request(srv):
    req = testing.request([], requestAttr=True)
    assert req.requestAttr
    req = testing.request([], session_attr=True)
    assert req.session.attr
    rh = {'Accept-Language': 'klingon'}
    req = testing.request([], responseHeaders=rh.items())
    assert req.responseHeaders == Headers({'accept-language': ['klingon']})
