# 20: Logins with authentication — The Pyramid Web Framework v2.0.2
Login views that authenticate a username and password against a list of users.

Background
-------------------------------------------------

Most web applications have URLs that allow people to add/edit/delete content via a web browser. Time to add [security](about:blank/narr/security.html#security-chapter) to the application. In this first step we introduce authentication. That is, logging in and logging out, using Pyramid's rich facilities for pluggable user storage.

In the next step we will introduce protection of resources with authorization security statements.

Objectives
-------------------------------------------------

*   Introduce the Pyramid concepts of authentication.
    
*   Create login and logout views.
    

Steps
---------------------------------------

1.  We are going to use the view classes step as our starting point:
    
    ```
cd ..; cp -r view_classes authentication; cd authentication

```

    
2.  Add `bcrypt` as a dependency in `authentication/setup.py`:
    
    ```
 1from setuptools import setup
 2
 3# List of dependencies installed via `pip install -e .`
 4# by virtue of the Setuptools `install_requires` value below.
 5requires = [
 6    'bcrypt',
 7    'pyramid',
 8    'pyramid_chameleon',
 9    'waitress',
10]
11
12# List of dependencies installed via `pip install -e ".[dev]"`
13# by virtue of the Setuptools `extras_require` value in the Python
14# dictionary below.
15dev_requires = [
16    'pyramid_debugtoolbar',
17    'pytest',
18    'webtest',
19]
20
21setup(
22    name='tutorial',
23    install_requires=requires,
24    extras_require={
25        'dev': dev_requires,
26    },
27    entry_points={
28        'paste.app_factory': [
29            'main = tutorial:main'
30        ],
31    },
32)

```

    
3.  We can now install our project in development mode:
    
    ```
$VENV/bin/pip install -e .

```

    
4.  Put the security hash in the `authentication/development.ini` configuration file as `tutorial.secret` instead of putting it in the code:
    
    ```
 1[app:main]
 2use = egg:tutorial
 3pyramid.reload_templates = true
 4pyramid.includes =
 5    pyramid_debugtoolbar
 6tutorial.secret = 98zd
 7
 8[server:main]
 9use = egg:waitress#main
10listen = localhost:6543

```

    
5.  Create an `authentication/tutorial/security.py` module that can find our user information by providing a [security policy](about:blank/glossary.html#term-security-policy):
    
    ```
 1import bcrypt
 2from pyramid.authentication import AuthTktCookieHelper
 3
 4
 5def hash_password(pw):
 6    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
 7    return pwhash.decode('utf8')
 8
 9def check_password(pw, hashed_pw):
10    expected_hash = hashed_pw.encode('utf8')
11    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
12
13
14USERS = {'editor': hash_password('editor'),
15         'viewer': hash_password('viewer')}
16
17
18class SecurityPolicy:
19    def __init__(self, secret):
20        self.authtkt = AuthTktCookieHelper(secret=secret)
21
22    def identity(self, request):
23        identity = self.authtkt.identify(request)
24        if identity is not None and identity['userid'] in USERS:
25            return identity
26
27    def authenticated_userid(self, request):
28        identity = self.identity(request)
29        if identity is not None:
30            return identity['userid']
31
32    def remember(self, request, userid, **kw):
33        return self.authtkt.remember(request, userid, **kw)
34
35    def forget(self, request, **kw):
36        return self.authtkt.forget(request, **kw)

```

    
6.  Register the `SecurityPolicy` with the [configurator](about:blank/glossary.html#term-configurator) in `authentication/tutorial/__init__.py`:
    
    ```
 1from pyramid.config import Configurator
 2
 3from .security import SecurityPolicy
 4
 5
 6def main(global_config, **settings):
 7    config = Configurator(settings=settings)
 8    config.include('pyramid_chameleon')
 9
10    config.set_security_policy(
11        SecurityPolicy(
12            secret=settings['tutorial.secret'],
13        ),
14    )
15
16    config.add_route('home', '/')
17    config.add_route('hello', '/howdy')
18    config.add_route('login', '/login')
19    config.add_route('logout', '/logout')
20    config.scan('.views')
21    return config.make_wsgi_app()

```

    
7.  Update the views in `authentication/tutorial/views.py`:
    
    ```
 1from pyramid.httpexceptions import HTTPFound
 2from pyramid.security import (
 3    remember,
 4    forget,
 5    )
 6
 7from pyramid.view import (
 8    view_config,
 9    view_defaults
10    )
11
12from .security import (
13    USERS,
14    check_password
15)
16
17
18@view_defaults(renderer='home.pt')
19class TutorialViews:
20    def __init__(self, request):
21        self.request = request
22        self.logged_in = request.authenticated_userid
23
24    @view_config(route_name='home')
25    def home(self):
26        return {'name': 'Home View'}
27
28    @view_config(route_name='hello')
29    def hello(self):
30        return {'name': 'Hello View'}
31
32    @view_config(route_name='login', renderer='login.pt')
33    def login(self):
34        request = self.request
35        login_url = request.route_url('login')
36        referrer = request.url
37        if referrer == login_url:
38            referrer = '/'  # never use login form itself as came_from
39        came_from = request.params.get('came_from', referrer)
40        message = ''
41        login = ''
42        password = ''
43        if 'form.submitted' in request.params:
44            login = request.params['login']
45            password = request.params['password']
46            hashed_pw = USERS.get(login)
47            if hashed_pw and check_password(password, hashed_pw):
48                headers = remember(request, login)
49                return HTTPFound(location=came_from,
50                                 headers=headers)
51            message = 'Failed login'
52
53        return dict(
54            name='Login',
55            message=message,
56            url=request.application_url + '/login',
57            came_from=came_from,
58            login=login,
59            password=password,
60        )
61
62    @view_config(route_name='logout')
63    def logout(self):
64        request = self.request
65        headers = forget(request)
66        url = request.route_url('home')
67        return HTTPFound(location=url,
68                         headers=headers)

```

    
8.  Add a login template at `authentication/tutorial/login.pt`:
    
    ```
 1<!DOCTYPE html>
 2<html lang="en">
 3<head>
 4    <title>Quick Tutorial: ${name}</title>
 5</head>
 6<body>
 7<h1>Login</h1>
 8<span tal:replace="message"/>
 9
10<form action="${url}" method="post">
11    <input type="hidden" name="came_from"
12           value="${came_from}"/>
13    <label for="login">Username</label>
14    <input type="text" id="login"
15           name="login"
16           value="${login}"/><br/>
17    <label for="password">Password</label>
18    <input type="password" id="password"
19           name="password"
20           value="${password}"/><br/>
21    <input type="submit" name="form.submitted"
22           value="Log In"/>
23</form>
24</body>
25</html>

```

    
9.  Provide a login/logout box in `authentication/tutorial/home.pt`:
    
    ```
 1<!DOCTYPE html>
 2<html lang="en">
 3<head>
 4    <title>Quick Tutorial: ${name}</title>
 5</head>
 6<body>
 7
 8<div>
 9    <a tal:condition="view.logged_in is None"
10            href="${request.application_url}/login">Log In</a>
11    <a tal:condition="view.logged_in is not None"
12            href="${request.application_url}/logout">Logout</a>
13</div>
14
15<h1>Hi ${name}</h1>
16<p>Visit <a href="${request.route_url('hello')}">hello</a></p>
17</body>
18</html>

```

    
10.  Run your Pyramid application with:
     
     ```
$VENV/bin/pserve development.ini --reload

```

     
11.  Open [http://localhost:6543/](http://localhost:6543/) in a browser.
     
12.  Click the "Log In" link.
     
13.  Submit the login form with the username `editor` and the password `editor`.
     
14.  Note that the "Log In" link has changed to "Logout".
     
15.  Click the "Logout" link.
     

Analysis
---------------------------------------------

Unlike many web frameworks, Pyramid includes a built-in but optional security model for authentication and authorization. This security system is intended to be flexible and support many needs. In this security model, authentication (who are you) and authorization (what are you allowed to do) are pluggable. To learn one step at a time, we provide a system that identifies users and lets them log out.

In this example we chose to use the bundled [`pyramid.authentication.AuthTktCookieHelper`](about:blank/api/authentication.html#pyramid.authentication.AuthTktCookieHelper "pyramid.authentication.AuthTktCookieHelper") helper to store the user's logged-in state in a cookie. We enabled it in our configuration and provided a ticket-signing secret in our INI file.

Our view class grew a login view. When you reached it via a `GET` request, it returned a login form. When reached via `POST`, it processed the submitted username and password against the `USERS` data store.

The function `hash_password` uses a one-way hashing algorithm with a salt on the user's password via `bcrypt`, instead of storing the password in plain text. This is considered to be a "best practice" for security.

Note

There are alternative libraries to `bcrypt` if it is an issue on your system. Just make sure that the library uses an algorithm approved for storing passwords securely.

The function `check_password` will compare the two hashed values of the submitted password and the user's password stored in the database. If the hashed values are equivalent, then the user is authenticated, else authentication fails.

Assuming the password was validated, we invoke [`pyramid.security.remember()`](about:blank/api/security.html#pyramid.security.remember "pyramid.security.remember") to generate a cookie that is set in the response. Subsequent requests return that cookie and identify the user.

In our template, we fetched the `logged_in` value from the view class. We use this to calculate the logged-in user, if any. In the template we can then choose to show a login link to anonymous visitors or a logout link to logged-in users.