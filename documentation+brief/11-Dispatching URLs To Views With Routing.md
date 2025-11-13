# 11: Dispatching URLs To Views With Routing — The Pyramid Web Framework v2.0.2
Routing matches incoming URL patterns to view code. Pyramid's routing has a number of useful features.

Background
-------------------------------------------------

Writing web applications usually means sophisticated URL design. We just saw some Pyramid machinery for requests and views. Let's look at features that help in routing.

Previously we saw the basics of routing URLs to views in Pyramid.

*   Your project's "setup" code registers a route name to be used when matching part of the URL
    
*   Elsewhere a view is configured to be called for that route name.
    

Note

Why do this twice? Other Python web frameworks let you create a route and associate it with a view in one step. As illustrated in [Routes need relative ordering](about:blank/designdefense.html#routes-need-ordering), multiple routes might match the same URL pattern. Rather than provide ways to help guess, Pyramid lets you be explicit in ordering. Pyramid also gives facilities to avoid the problem. It's relatively easy to build a system that uses implicit route ordering with Pyramid too. See [The Groundhog series of screencasts](https://web.archive.org/web/20190118040819/http://static.repoze.org/casts/videotags.html) if you're interested in doing so.

Objectives
-------------------------------------------------

*   Define a route that extracts part of the URL into a Python dictionary.
    
*   Use that dictionary data in a view.
    

Steps
---------------------------------------

1.  First we copy the results of the `view_classes` step:
    
    ```
cd ..; cp -r view_classes routing; cd routing
$VENV/bin/pip install -e .

```

    
2.  Our `routing/tutorial/__init__.py` needs a route with a replacement pattern:
    
    ```
1from pyramid.config import Configurator
2
3
4def main(global_config, **settings):
5    config = Configurator(settings=settings)
6    config.include('pyramid_chameleon')
7    config.add_route('home', '/howdy/{first}/{last}')
8    config.scan('.views')
9    return config.make_wsgi_app()

```

    
3.  We just need one view in `routing/tutorial/views.py`:
    
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
12    @view_config(route_name='home')
13    def home(self):
14        first = self.request.matchdict['first']
15        last = self.request.matchdict['last']
16        return {
17            'name': 'Home View',
18            'first': first,
19            'last': last
20        }

```

    
4.  We just need one view in `routing/tutorial/home.pt`:
    
    ```
 1<!DOCTYPE html>
 2<html lang="en">
 3<head>
 4    <title>Quick Tutorial: ${name}</title>
 5</head>
 6<body>
 7<h1>${name}</h1>
 8<p>First: ${first}, Last: ${last}</p>
 9</body>
10</html>

```

    
5.  Update `routing/tutorial/tests.py`:
    
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
14        from .views import TutorialViews
15
16        request = testing.DummyRequest()
17        request.matchdict['first'] = 'First'
18        request.matchdict['last'] = 'Last'
19        inst = TutorialViews(request)
20        response = inst.home()
21        self.assertEqual(response['first'], 'First')
22        self.assertEqual(response['last'], 'Last')
23
24
25class TutorialFunctionalTests(unittest.TestCase):
26    def setUp(self):
27        from tutorial import main
28        app = main({})
29        from webtest import TestApp
30
31        self.testapp = TestApp(app)
32
33    def test_home(self):
34        res = self.testapp.get('/howdy/Jane/Doe', status=200)
35        self.assertIn(b'Jane', res.body)
36        self.assertIn(b'Doe', res.body)

```

    
6.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
..
2 passed in 0.39 seconds

```

    
7.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
8.  Open [http://localhost:6543/howdy/amy/smith](http://localhost:6543/howdy/amy/smith) in your browser.
    

Analysis
---------------------------------------------

In `__init__.py` we see an important change in our route declaration:

```
config.add_route('hello', '/howdy/{first}/{last}')

```


With this we tell the [configurator](about:blank/glossary.html#term-configurator) that our URL has a "replacement pattern". With this, URLs such as `/howdy/amy/smith` will assign `amy` to `first` and `smith` to `last`. We can then use this data in our view:

```
self.request.matchdict['first']
self.request.matchdict['last']

```


`request.matchdict` contains values from the URL that match the "replacement patterns" (the curly braces) in the route declaration. This information can then be used anywhere in Pyramid that has access to the request.