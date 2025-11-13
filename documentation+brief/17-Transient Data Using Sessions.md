# 17: Transient Data Using Sessions — The Pyramid Web Framework v2.0.2
Store and retrieve non-permanent data in Pyramid sessions.

Background
-------------------------------------------------

When people use your web application, they frequently perform a task that requires semi-permanent data to be saved. For example, a shopping cart. This is called a [session](about:blank/glossary.html#term-session).

Pyramid has basic built-in support for sessions. Third party packages such as [pyramid\_redis\_sessions](https://github.com/ericrasmussen/pyramid_redis_sessions) provide richer session support. Or you can create your own custom sessioning engine. Let's take a look at the [built-in sessioning support](../narr/sessions.html).

Objectives
-------------------------------------------------

*   Make a session factory using a built-in, simple Pyramid sessioning system.
    
*   Change our code to use a session.
    

Steps
---------------------------------------

1.  First we copy the results of the `view_classes` step:
    
    ```
cd ..; cp -r view_classes sessions; cd sessions
$VENV/bin/pip install -e .

```

    
2.  Our `sessions/tutorial/__init__.py` needs a choice of session factory to get registered with the [configurator](about:blank/glossary.html#term-configurator):
    
    ```
 1from pyramid.config import Configurator
 2from pyramid.session import SignedCookieSessionFactory
 3
 4
 5def main(global_config, **settings):
 6    my_session_factory = SignedCookieSessionFactory(
 7        'itsaseekreet')
 8    config = Configurator(settings=settings,
 9                          session_factory=my_session_factory)
10    config.include('pyramid_chameleon')
11    config.add_route('home', '/')
12    config.add_route('hello', '/howdy')
13    config.scan('.views')
14    return config.make_wsgi_app()

```

    
3.  Our views in `sessions/tutorial/views.py` can now use `request.session`:
    
    ```
 1from pyramid.view import (
 2    view_config,
 3    view_defaults
 4    )
 5
 6
 7@view_defaults(renderer='home.pt')
 8class TutorialViews:
 9    def __init__(self, request):
10        self.request = request
11
12    @property
13    def counter(self):
14        session = self.request.session
15        if 'counter' in session:
16            session['counter'] += 1
17        else:
18            session['counter'] = 1
19
20        return session['counter']
21
22
23    @view_config(route_name='home')
24    def home(self):
25        return {'name': 'Home View'}
26
27    @view_config(route_name='hello')
28    def hello(self):
29        return {'name': 'Hello View'}

```

    
4.  The template at `sessions/tutorial/home.pt` can display the value:
    
    ```
 1<!DOCTYPE html>
 2<html lang="en">
 3<head>
 4    <title>Quick Tutorial: ${name}</title>
 5</head>
 6<body>
 7<h1>Hi ${name}</h1>
 8<p>Count: ${view.counter}</p>
 9</body>
10</html>

```

    
5.  Make sure the tests still pass:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
....
4 passed in 0.42 seconds

```

    
6.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
7.  Open [http://localhost:6543/](http://localhost:6543/) and [http://localhost:6543/howdy](http://localhost:6543/howdy) in your browser. As you reload and switch between those URLs, note that the counter increases and is _not_ specific to the URL.
    
8.  Restart the application and revisit the page. Note that counter still increases from where it left off.
    

Analysis
---------------------------------------------

Pyramid's [request](about:blank/glossary.html#term-request) object now has a `session` attribute that we can use in our view code. It acts like a dictionary.

Since all the views are using the same counter, we made the counter a Python property at the view class level. With this, each reload will increase the counter displayed in our template.

In web development, "flash messages" are notes for the user that need to appear on a screen after a future web request. For example, when you add an item using a form `POST`, the site usually issues a second HTTP Redirect web request to view the new item. You might want a message to appear after that second web request saying "Your item was added." You can't just return it in the web response for the POST, as it will be tossed out during the second web request.

Flash messages are a technique where messages can be stored between requests, using sessions, then removed when they finally get displayed.