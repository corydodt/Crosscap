# crosscap.permitting API: implement authorization for your web app or service


These examples demonstrate how to implement permitting in your Tornado- or Klein-based app.

## To use:

1. Run either `./tornadoauth.py` or `./kleinauth.py`.

2. In another window/tab, use an HTTP client like curl to request `http://localhost:8888/`

   This will print out keys for alice and bob.

   You can confirm, if you like, that you cannot access `/user` or `/admin` without a valid token
   in the Authorization header.

3. Using your HTTP client, set a header for `Authorization: bearer xxxxxx` and fill in either alice's
   token or bob's token in place of `xxxxxx`. Confirm, if you like, that alice can access every URL
   but bob is denied access to `/admin`.

### Demo

(asciinema link here)

## Common features of the example apps

A single, common User instance and "user database" (just a dict in our example) are provided under the package directory `myapp`.

Both apps have two users:

- `alice`, an admin
- `bob`, an ordinary user

(Since both apps have exactly the same "user database" and the same concept of user access in general,
the `authenticate` method in the examples is identical between the two.)

Both apps expose three URLs:

- `/` (the root URL), which prints out a message and also prints out new tokens for both users 
- `/user`, a resource that prints a message containing the username of the
 accessing user. This resource can be accessed by any logged-in user, but not
 by an unauthenticated (anonymous) user.
- `/admin`, a resource that can only be accessed by a user possessing the `admin` role.

Both apps implement `ICurrentUser` as the adapter `AuthUser`, but in different ways (described below).


## Tornado

In `tornadoauth.py`,

1. The service routes are implemented as subclasses of RequestHandler, and only `get` is implemented. Here,
 the `permits()` decorator goes above each get method. If you had other methods in the RequestHandler (`post`, for
 example) they would need their own decorators, as they have their own permissions.

2. In Tornado, `AuthUser` methods are impelemented using the RequestHandler API:

    - The `Authorization` header comes from `RequestHandler.request.headers`
    - 403 is signalled to the client using `RequestHandler.send_error`
    - To feel more familiar to Tornado users, we set the user object as `RequestHandler.current_user`

3. We register an adapter so instances of RequestHandler can be adapted to ICurrentUser via the AuthUser class.

4. We set up a pretty standard Tornado main function which exposes the three URLs and turns on pretty logging.


## Klein

In `kleinauth.py`,

1. The service routes are implemented as Klein `@route`s. The `permits()` decorator goes on each route.

2. In Klein, `AuthUser` methods are impelemented using the `twisted.web.server.Request` API:

    - The `Authorization` header comes from `Request.requestHeaders.getRawHeaders()`
    - 403 is signalled to the client by raising `Forbidden()`
    - The user object is set on the Session object, and accessed with `getSession().user`.

3. We register an adapter so instances of Request can be adapted to ICurrentUser via the AuthUser class.

4. We turn off traceback display on the Site object (recommended for all Twisted.web-based services.)


## Out of scope: user login

One thing not covered in these examples (or, indeed, by `permitting` itself) is
password storage/checking, so no aspect of user login is covered.

Permitting is for token-based auth when a user *already has a token*. There
are many ways the user or service client can get this token:

- Username+password login. In an interactive web app (or an app that supports
 basic auth at the service level), a user can login with a password, and, in
 the response, get a JWT to use for future requests. A single-page web app
 might use this method, providing the token in each future request through
 javascript. (You can also add MFA here if you like, the approach is the same
 from `permitting`'s point of view.)
 
   Browser-based interactive apps could also respond with a `Set-Cookie` header
 and, in following requests, read the token from the cookie instead of the
 `authorization` header. In permitting, you can change where you get the
 token by implementing a property for `ICurrentUser.token`.

- BYOT (bring your own token). In this scenario, a (probably **not**
 interactive, **not** HTML) client generates the JWT and submits it
 along with every request. In this scenario the client must have a shared
 (potentially revokable) secret with your service. Secret-storage services
 might help here to hold the shared secret (e.g. Kubernetes Secrets, Vault,
 Amazon Secrets Manager)--or the secret might simply be pre-shared.

   Since `permitting` provides `create_timed_token`, a client written in
 Python could use `permitting` to generate its tokens.

- A token generation service. Similar to BYOT, except this external service
 (not the client) holds the shared secret, and the external service
 issues the token to the client instead of expecting the client to generate
 it.
