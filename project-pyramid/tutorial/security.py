import bcrypt
from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import ACLHelper, Authenticated, Everyone


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
    return hashed.decode("utf8")


def check_password(password: str, hashed_password: str) -> bool:
    expected = hashed_password.encode("utf8")
    return bcrypt.checkpw(password.encode("utf8"), expected)


USERS = {
    "editor": hash_password("editor"),
    "viewer": hash_password("viewer"),
}

GROUPS = {
    "editor": ["group:editors"],
}


class SecurityPolicy:
    def __init__(self, secret: str):
        self.authtkt = AuthTktCookieHelper(secret=secret)
        self.acl_helper = ACLHelper()

    def identity(self, request):
        identity = self.authtkt.identify(request)
        if identity is not None and identity["userid"] in USERS:
            return identity

    def authenticated_userid(self, request):
        identity = self.identity(request)
        if identity is not None:
            return identity["userid"]

    def remember(self, request, userid, **kw):
        return self.authtkt.remember(request, userid, **kw)

    def forget(self, request, **kw):
        return self.authtkt.forget(request, **kw)

    def permits(self, request, context, permission):
        principals = self.effective_principals(request)
        return self.acl_helper.permits(context, principals, permission)

    def effective_principals(self, request):
        principals = [Everyone]
        userid = self.authenticated_userid(request)
        if userid is not None:
            principals.append(Authenticated)
            principals.append(f"u:{userid}")
            principals.extend(GROUPS.get(userid, []))
        return principals
