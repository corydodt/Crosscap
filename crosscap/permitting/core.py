"""
A framework for authorizing HTTP traffic in a Klein-based web service

## Assumptions

- your app will use JWT
- your app will figure out how to deliver the token to the client. This may involve a login page, for example.
- your framework uses a request object with a .write() method

## You must:

- use the permits() decorator, and implement forbidden and (optionally) success
- have a user object, implemented however you want.
- implement a way to generate tokens from the user object; create_timed_token may be helpful
- implement ICurrentUser
    - implement .token by getting the JWT string from your request object. extract_bearer_token may be helpful
    - implement .authenticate to check the JWT and return a user instance. validate_token may be helpful
    - implement .authenticated to receive the authenticated user and do something with it
    - implement .forbidden to receive the authenticated user and do something with it
    - implement .roles to produce a sequence of the roles possessed by a user.
"""
from datetime import datetime, timedelta
import re

import jwt

import wrapt

from crosscap.interface import ICurrentUser


JWT_ALGO = ('HS256',)
JWT_DURATION = 600 # 10 minutes


def role_in(roles_allowed):
    """
    A permission checker that checks that a role possessed by the user matches one of the role_in list
    """
    def _check_with_authuser(authuser):
        return any(r in authuser.roles for r in roles_allowed)
    
    return _check_with_authuser


def permits(*rules):
    """
    Allow access to this resource if 
    1. the user is authenticated, and
    2. the specified security factors are satisfied.

    - rules: a list of callables. each callable must take the authuser as an argument and return True or False
    - forbidden: a callable which will be called with the handler object, and the result returned, for a 403/Forbidden message
    - authenticated: a callable which will be called with the handler and user object, after authentication is checked but before authorization
    """
    def _do_authentication(authuser):
        u = authuser.authenticate()
        if not u:
            return None

        # call the authenticated handler BEFORE checking authorization, so there is a user
        # to check permissions rules against
        return authuser.authenticated(u)

    def _do_authorization(authuser, user):
        return all(rule(authuser) for rule in rules)
        
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # we're looking for a request object, which presumably has a `.write()` method.
        if hasattr(instance, 'write') and callable(instance.write):
            handler = instance
        else:
            # for methods that are passed the request handler in the first argument, do this
            handler = (lambda handler, *a, **kw: handler)(*args, **kwargs)

        authuser = ICurrentUser(handler)

        # is the user found? (authenticated?)
        user = _do_authentication(authuser)
        if not user:
            return authuser.forbidden()

        # user found, but are they authorized for this resource?
        if not _do_authorization(authuser, user):
            return authuser.forbidden()

        # all checks pass, return the resource
        return wrapped(*args, **kwargs)

    return wrapper


def _assert_stringy(**kwargs):
    """
    Raise TypeError when s is not stringy or is empty, displaying `label' in the error
    
    A convenience check. A number of APIs in this file must return None on bad input,
    but we can still do type checks to catch programming errors.
    """
    for label, s in kwargs.items():
        if type(s) not in (str, bytes) or len(s) == 0:
            raise TypeError("{label} {s!r} must be str/bytes and non-empty".format(label=label, s=s))


def validate_token(token, secret, **kwargs):
    """
    Check a token signature and claims, and return the userid string (`sub` claim) or None
    """
    _assert_stringy(token=token, secret=secret)
    kwargs.setdefault('algorithms', [JWT_ALGO[0]])
    try:
        payload = jwt.decode(token, secret, **kwargs)
        return payload['sub']
    except (jwt.exceptions.PyJWTError, KeyError):
        return None


BEARER_RX = re.compile(r'bearer\s+(?P<token>\S+)', re.I)

def extract_bearer_token(header_value):
    """
    For the common "Authorization: bearer token" case, extract JWT from the authorization header
    """
    _assert_stringy(header_value=header_value)
    match = BEARER_RX.match(header_value)
    return match.group('token') if match else None


def create_timed_token(sub, secret, duration=JWT_DURATION, **kwargs):
    """
    Convenience method to create tokens of a particular duration

    You can also create non-expiring tokens by setting duration=None
    """
    _assert_stringy(sub=sub, secret=secret)
    kwargs.setdefault('algorithm', JWT_ALGO[0])

    payload = {'sub': sub}
    if duration is not None:
        payload.update({'exp': _expiration(duration)})

    t = jwt.encode(payload, secret, **kwargs)

    # Make sure we created a usable token.
    # validate and create are slightly asymmetric in that you can allow multiple algorithms
    # during decode, but only one during encode, so swap these around
    validate_kwargs = kwargs.copy()
    validate_kwargs.setdefault('algorithms', [validate_kwargs.pop('algorithm')])
    validate_kwargs.setdefault('leeway', 1)
    assert validate_token(t, secret, **validate_kwargs)

    return t


def _expiration(duration):
    """
    Generate a datetime now + duration seconds
    """
    return datetime.utcnow() + timedelta(seconds=duration)
