# 21: Protecting Resources With Authorization — The Pyramid Web Framework v2.0.2
Assign security statements to resources describing the permissions required to perform an operation.

Background
-------------------------------------------------

Our application has URLs that allow people to add/edit/delete content via a web browser. Time to add security to the application. Let's protect our add/edit views to require a login (username of `editor` and password of `editor`). We will allow the other views to continue working without a password.

Objectives
-------------------------------------------------

*   Introduce the Pyramid concepts of authentication, authorization, permissions, and access control lists (ACLs).
    
*   Make a [root factory](about:blank/glossary.html#term-root-factory) that returns an instance of our class for the top of the application.
    
*   Assign security statements to our root resource.
    
*   Add a permissions predicate on a view.
    
*   Provide a [Forbidden view](about:blank/glossary.html#term-Forbidden-view) to handle visiting a URL without adequate permissions.
    

Steps
---------------------------------------

1.  We are going to use the authentication step as our starting point:
    
    ```
cd ..; cp -r authentication authorization; cd authorization
$VENV/bin/pip install -e .

```

    
2.  Start by changing `authorization/tutorial/__init__.py` to specify a root factory to the [configurator](about:blank/glossary.html#term-configurator):
    
    ```
 1from pyramid.config import Configurator
 2
 3from .security import SecurityPolicy
 4
 5
 6def main(global_config, **settings):
 7    config = Configurator(settings=settings,
 8                          root_factory='.resources.Root')
 9    config.include('pyramid_chameleon')
10
11    config.set_security_policy(
12        SecurityPolicy(
13            secret=settings['tutorial.secret'],
14        ),
15    )
16
17    config.add_route('home', '/')
18    config.add_route('hello', '/howdy')
19    config.add_route('login', '/login')
20    config.add_route('logout', '/logout')
21    config.scan('.views')
22    return config.make_wsgi_app()

```

    
3.  That means we need to implement `authorization/tutorial/resources.py`:
    
    ```
1from pyramid.authorization import Allow, Everyone
2
3
4class Root:
5    __acl__ = [(Allow, Everyone, 'view'),
6               (Allow, 'group:editors', 'edit')]
7
8    def __init__(self, request):
9        pass

```

    
4.  Define a `GROUPS` data store and the `permits` method of our `SecurityPolicy`:
    
    ```
 1import bcrypt
 2from pyramid.authentication import AuthTktCookieHelper
 3from pyramid.authorization import (
 4    ACLHelper,
 5    Authenticated,
 6    Everyone,
 7)
 8
 9
10def hash_password(pw):
11    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
12    return pwhash.decode('utf8')
13
14def check_password(pw, hashed_pw):
15    expected_hash = hashed_pw.encode('utf8')
16    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
17
18
19USERS = {'editor': hash_password('editor'),
20         'viewer': hash_password('viewer')}
21GROUPS = {'editor': ['group:editors']}
22
23
24class SecurityPolicy:
25    def __init__(self, secret):
26        self.authtkt = AuthTktCookieHelper(secret=secret)
27        self.acl = ACLHelper()
28
29    def identity(self, request):
30        identity = self.authtkt.identify(request)
31        if identity is not None and identity['userid'] in USERS:
32            return identity
33
34    def authenticated_userid(self, request):
35        identity = self.identity(request)
36        if identity is not None:
37            return identity['userid']
38
39    def remember(self, request, userid, **kw):
40        return self.authtkt.remember(request, userid, **kw)
41
42    def forget(self, request, **kw):
43        return self.authtkt.forget(request, **kw)
44
45    def permits(self, request, context, permission):
46        principals = self.effective_principals(request)
47        return self.acl.permits(context, principals, permission)
48
49    def effective_principals(self, request):
50        principals = [Everyone]
51        userid = self.authenticated_userid(request)
52        if userid is not None:
53            principals += [Authenticated, 'u:' + userid]
54            principals += GROUPS.get(userid, [])
55        return principals

```

    
5.  Change `authorization/tutorial/views.py` to require the `edit` permission on the `hello` view and implement the forbidden view:
    
    ```
 1from pyramid.httpexceptions import HTTPFound
 2from pyramid.security import (
 3    remember,
 4    forget,
 5)
 6
 7from pyramid.view import (
 8    view_config,
 9    view_defaults,
10    forbidden_view_config
11)
12
13from .security import (
14    USERS,
15    check_password
16)
17
18
19@view_defaults(renderer='home.pt')
20class TutorialViews:
21    def __init__(self, request):
22        self.request = request
23        self.logged_in = request.authenticated_userid
24
25    @view_config(route_name='home')
26    def home(self):
27        return {'name': 'Home View'}
28
29    @view_config(route_name='hello', permission='edit')
30    def hello(self):
31        return {'name': 'Hello View'}
32
33    @view_config(route_name='login', renderer='login.pt')
34    @forbidden_view_config(renderer='login.pt')
35    def login(self):
36        request = self.request
37        login_url = request.route_url('login')
38        referrer = request.url
39        if referrer == login_url:
40            referrer = '/'  # never use login form itself as came_from
41        came_from = request.params.get('came_from', referrer)
42        message = ''
43        login = ''
44        password = ''
45        if 'form.submitted' in request.params:
46            login = request.params['login']
47            password = request.params['password']
48            hashed_pw = USERS.get(login)
49            if hashed_pw and check_password(password, hashed_pw):
50                headers = remember(request, login)
51                return HTTPFound(location=came_from,
52                                 headers=headers)
53            message = 'Failed login'
54
55        return dict(
56            name='Login',
57            message=message,
58            url=request.application_url + '/login',
59            came_from=came_from,
60            login=login,
61            password=password,
62        )
63
64    @view_config(route_name='logout')
65    def logout(self):
66        request = self.request
67        headers = forget(request)
68        url = request.route_url('home')
69        return HTTPFound(location=url,
70                         headers=headers)

```

    
6.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
7.  Open [http://localhost:6543/](http://localhost:6543/) in a browser.
    
8.  If you are still logged in, click the "Log Out" link.
    
9.  Visit [http://localhost:6543/howdy](http://localhost:6543/howdy) in a browser. You should be asked to login.
    

Analysis
---------------------------------------------

This simple tutorial step can be boiled down to the following:

*   A view can require a _permission_ (`edit`).
    
*   The context for our view (the `Root`) has an access control list (ACL).
    
*   This ACL says that the `edit` permission is available on `Root` to the `group:editors` _principal_.
    
*   The `SecurityPolicy.effective_principals` method answers whether a particular user (`editor`) is a member of a particular group (`group:editors`).
    
*   The `SecurityPolicy.permits` method is invoked when Pyramid wants to know whether the user is allowed to do something. To do this, it uses the [`pyramid.authorization.ACLHelper`](about:blank/api/authorization.html#pyramid.authorization.ACLHelper "pyramid.authorization.ACLHelper") to inspect the ACL on the `context` and determine if the request is allowed or denied the specific permission.
    

In summary, `hello` wants `edit` permission, `Root` says `group:editors` has `edit` permission.

Of course, this only applies on `Root`. Some other part of the site (a.k.a. _context_) might have a different ACL.

If you are not logged in and visit `/howdy`, you need to get shown the login screen. How does Pyramid know what is the login page to use? We explicitly told Pyramid that the `login` view should be used by decorating the view with `@forbidden_view_config`.