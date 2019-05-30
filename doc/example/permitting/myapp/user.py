"""
A generic user class for generic apps
"""
import attr


USER_ALICE = 'alice'
USER_BOB = 'bob'
ROLE_ADMIN = 'admin'


@attr.s
class User(object):
    """
    I am a service level user. I have an id and roles.
    """
    userID = attr.ib(type=str)
    roles = attr.ib(default=attr.Factory(list))


USER_DATABASE = {
    # alice is an admin
    USER_ALICE: User('alice', roles=[ROLE_ADMIN]),

    # bob is not
    USER_BOB: User('bob', roles=[]),
}


