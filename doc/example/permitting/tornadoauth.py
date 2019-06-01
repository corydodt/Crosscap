#!/usr/bin/env python
"""
JWT-based auth for a Tornado service
"""
import inspect
import os

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.log import enable_pretty_logging

from twisted.python import components

from zope.interface import implementer

from crosscap import permitting as pm

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
        uid = pm.validate_token(self.token, TOKEN_SECRET, {}).get('sub')
        return USER_DATABASE.get(uid)

    @property
    def token(self):
        hdr = self.handler.request.headers.get('authorization', None)
        if hdr:
            return pm.extract_bearer_token(hdr)

    @property
    def roles(self):
        return getattr(self.handler.current_user, 'roles', ())

    def forbidden(self):
        """
        Produce an error 403 when an unauthorized request happens
        """
        self.handler.send_error(403)

    def authenticated(self, user):
        """
        When a user successfully authenticates, do this
        """
        self.handler.current_user = user
        return user

components.registerAdapter(AuthUser, RequestHandler, pm.ICurrentUser)


class AdminOnlyHandler(RequestHandler):
    """
    A resource that requires admin rights
    """
    @pm.permits(pm.role_in([ROLE_ADMIN]))
    def get(self):
        uid = self.current_user.userID
        self.write(f"for admin ({uid}) eyes only: 👀")


class AnyUserHandler(RequestHandler):
    """
    A resource that requires any logged-in user
    """
    @pm.permits()
    def get(self):
        uid = self.current_user.userID
        self.write(f"your username is {uid}")


class PublicHandler(RequestHandler):
    """
    Root(/) method prints a message and 2 tokens, visible to everyone without auth
    """
    def get(self):
        bob = pm.create_timed_token('bob', TOKEN_SECRET).decode('utf-8')
        alice = pm.create_timed_token('alice', TOKEN_SECRET).decode('utf-8')
        ret = inspect.cleandoc(f"""
            Hello, 🌎. Here are some tokens:
            bob: {bob}
            alice: {alice}
            """)

        self.write(ret)


def main(port):
    """
    Run the web app.
    """
    app = Application([
        (r"/", PublicHandler),
        (r"/admin", AdminOnlyHandler),
        (r"/user", AnyUserHandler),
    ])
    enable_pretty_logging()
    print('_' * 25, "listening on", port, '_' * 25)
    app.listen(port)
    IOLoop.current().start()


if __name__ == '__main__':
    main(8888)
