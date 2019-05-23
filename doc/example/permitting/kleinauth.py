#!/usr/bin/env python
"""
JWT-based auth for a Klein-based service
"""
import inspect
import os

from werkzeug.exceptions import Forbidden

from klein import Klein, route

from zope.interface import implementer

from twisted.python.components import registerAdapter
from twisted.web.server import Request, Site

import crosscap.permitting as pm

from myapp.user import ROLE_ADMIN, USER_DATABASE


TOKEN_SECRET = os.environ.get('TOKEN_SECRET')
assert TOKEN_SECRET, "** Please set the environment variable: TOKEN_SECRET=...."


@implementer(pm.ICurrentUser)
class AuthUser(object):
    def __init__(self, handler):
        self.handler = handler

    def authenticate(self):
        """
        Unpack a JWT and confirm the user's identity, 
        """
        uid = pm.validate_token(self.token, TOKEN_SECRET)
        return USER_DATABASE.get(uid)

    @property
    def token(self):
        hdr = self.handler.requestHeaders.getRawHeaders('authorization', [None])[0]
        if hdr:
            return pm.extract_bearer_token(hdr)

    @property
    def roles(self):
        return self.handler.getSession().user.roles

    def forbidden(self):
        """
        Produce an error 403 when an unauthorized request happens
        """
        raise Forbidden()

    def authenticated(self, user):
        """
        When a user successfully authenticates, do this
        """
        self.handler.getSession().user = user
        return user

registerAdapter(AuthUser, Request, pm.ICurrentUser)


app = Klein()


@app.route('/')
def public(request):
    """
    Root(/) method prints a message and 2 tokens, visible to everyone without auth
    """
    request.setHeader('content-type', 'text/plain; charset=utf-8')
    bob = pm.create_timed_token('bob', TOKEN_SECRET).decode('utf-8')
    alice = pm.create_timed_token('alice', TOKEN_SECRET).decode('utf-8')

    ret = inspect.cleandoc(f"""
        Hello, 🌎. Here are some tokens:
        bob: {bob}
        alice: {alice}
        """)
    return ret


@app.route('/user')
@pm.permits()
def user(request):
    """
    A resource that requires any logged-in user
    """
    uid = request.getSession().user.userID
    return f"your username is {uid}"


@app.route('/admin')
@pm.permits(pm.role_in([ROLE_ADMIN]))
def admin(request):
    """
    A resource that requires admin rights
    """
    uid = request.getSession().user.userID
    return f'for admin ({uid}) eyes only: 👀'


if __name__ == '__main__':
    Site.displayTracebacks = False
    app.run("localhost", 8888)
