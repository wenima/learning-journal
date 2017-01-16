import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated
from pyramid.security import Allow
from pyramid.session import SignedCookieSessionFactory

class MyRoot(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'secret'),
    ]

def check_credentials(username, password):
    if username and password:
        if username == os.environ["AUTH_USERNAME"]:
            if password == os.environ["AUTH_PASSWORD"]:
                return True
    return False

def includeme(config):
    """security-related configuration"""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(MyRoot)
    #guard againset CSRF
    session_secret = os.environ.get("SESSION SECRET", 'itsaseekrit')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
