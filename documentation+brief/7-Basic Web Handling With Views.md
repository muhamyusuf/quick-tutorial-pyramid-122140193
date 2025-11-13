# 07: Basic Web Handling With Views — The Pyramid Web Framework v2.0.2
Organize a views module with decorators and multiple views.

Background
-------------------------------------------------

For the examples so far, the `hello_world` function is a "view". In Pyramid, views are the primary way to accept web requests and return responses.

So far our examples place everything in one file:

*   The view function
    
*   Its registration with the configurator
    
*   The route to map it to a URL
    
*   The WSGI application launcher
    

Let's move the views out to their own `views.py` module and change our startup code to scan that module, looking for decorators that set up the views. Let's also add a second view and update our tests.

Objectives
-------------------------------------------------

*   Move views into a module that is scanned by the configurator.
    
*   Create decorators that do declarative configuration.
    

Steps
---------------------------------------

1.  Let's begin by using the previous package as a starting point for a new distribution, then making it active:
    
    ```
cd ..; cp -r functional_testing views; cd views
$VENV/bin/pip install -e .

```

    
2.  Our `views/tutorial/__init__.py` gets a lot shorter:
    
    ```
1from pyramid.config import Configurator
2
3
4def main(global_config, **settings):
5    config = Configurator(settings=settings)
6    config.add_route('home', '/')
7    config.add_route('hello', '/howdy')
8    config.scan('.views')
9    return config.make_wsgi_app()

```

    
3.  Let's add a module `views/tutorial/views.py` that is focused on handling requests and responses:
    
    ```
 1from pyramid.response import Response
 2from pyramid.view import view_config
 3
 4
 5# First view, available at http://localhost:6543/
 6@view_config(route_name='home')
 7def home(request):
 8    return Response('<body>Visit <a href="/howdy">hello</a></body>')
 9
10
11# /howdy
12@view_config(route_name='hello')
13def hello(request):
14    return Response('<body>Go back <a href="/">home</a></body>')

```

    
4.  Update the tests to cover the two new views:
    
    ```
 1import unittest
 2
 3from pyramid import testing
 4
 5
 6class TutorialViewTests(unittest.TestCase):
 7    def setUp(self):
 8        self.config = testing.setUp()
 9
10    def tearDown(self):
11        testing.tearDown()
12
13    def test_home(self):
14        from .views import home
15
16        request = testing.DummyRequest()
17        response = home(request)
18        self.assertEqual(response.status_code, 200)
19        self.assertIn(b'Visit', response.body)
20
21    def test_hello(self):
22        from .views import hello
23
24        request = testing.DummyRequest()
25        response = hello(request)
26        self.assertEqual(response.status_code, 200)
27        self.assertIn(b'Go back', response.body)
28
29
30class TutorialFunctionalTests(unittest.TestCase):
31    def setUp(self):
32        from tutorial import main
33        app = main({})
34        from webtest import TestApp
35
36        self.testapp = TestApp(app)
37
38    def test_home(self):
39        res = self.testapp.get('/', status=200)
40        self.assertIn(b'<body>Visit', res.body)
41
42    def test_hello(self):
43        res = self.testapp.get('/howdy', status=200)
44        self.assertIn(b'<body>Go back', res.body)

```

    
5.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
....
4 passed in 0.28 seconds

```

    
6.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
7.  Open [http://localhost:6543/](http://localhost:6543/) and [http://localhost:6543/howdy](http://localhost:6543/howdy) in your browser.
    

Analysis
---------------------------------------------

We added some more URLs, but we also removed the view code from the application startup code in `tutorial/__init__.py`. Our views, and their view registrations (via decorators) are now in a module `views.py`, which is scanned via `config.scan('.views')`.

We have two views, each leading to the other. If you start at [http://localhost:6543/](http://localhost:6543/), you get a response with a link to the next view. The `hello` view (available at the URL `/howdy`) has a link back to the first view.

This step also shows that the name appearing in the URL, the name of the "route" that maps a URL to a view, and the name of the view, can all be different. More on routes later.

Earlier we saw `config.add_view` as one way to configure a view. This section introduces `@view_config`. Pyramid's configuration supports [imperative configuration](about:blank/glossary.html#term-imperative-configuration), such as the `config.add_view` in the previous example. You can also use [declarative configuration](about:blank/glossary.html#term-declarative-configuration), in which a Python [decorator](https://docs.python.org/3/glossary.html#term-decorator "(in Python v3.11)") is placed on the line above the view. Both approaches result in the same final configuration, thus usually, it is simply a matter of taste.