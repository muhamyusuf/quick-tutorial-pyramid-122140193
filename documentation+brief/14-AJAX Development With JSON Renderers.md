# 14: AJAX Development With JSON Renderers — The Pyramid Web Framework v2.0.2
Modern web apps are more than rendered HTML. Dynamic pages now use JavaScript to update the UI in the browser by requesting server data as JSON. Pyramid supports this with a _JSON renderer_.

Background
-------------------------------------------------

As we saw in [08: HTML Generation With Templating](templating.html), view declarations can specify a renderer. Output from the view is then run through the renderer, which generates and returns the response. We first used a Chameleon renderer, then a Jinja2 renderer.

Renderers aren't limited, however, to templates that generate HTML. Pyramid supplies a JSON renderer which takes Python data, serializes it to JSON, and performs some other functions such as setting the content type. In fact you can write your own renderer (or extend a built-in renderer) containing custom logic for your unique application.

Steps
---------------------------------------

1.  First we copy the results of the `view_classes` step:
    
    ```
cd ..; cp -r view_classes json; cd json
$VENV/bin/pip install -e .

```

    
2.  We add a new route for `hello_json` in `json/tutorial/__init__.py`:
    
    ```
 1from pyramid.config import Configurator
 2
 3
 4def main(global_config, **settings):
 5    config = Configurator(settings=settings)
 6    config.include('pyramid_chameleon')
 7    config.add_route('home', '/')
 8    config.add_route('hello', '/howdy')
 9    config.add_route('hello_json', '/howdy.json')
10    config.scan('.views')
11    return config.make_wsgi_app()

```

    
3.  Rather than implement a new view, we will "stack" another decorator on the `hello` view in `views.py`:
    
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
14        return {'name': 'Home View'}
15
16    @view_config(route_name='hello')
17    @view_config(route_name='hello_json', renderer='json')
18    def hello(self):
19        return {'name': 'Hello View'}

```

    
4.  We need a new functional test at the end of `json/tutorial/tests.py`:
    
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
17        inst = TutorialViews(request)
18        response = inst.home()
19        self.assertEqual('Home View', response['name'])
20
21    def test_hello(self):
22        from .views import TutorialViews
23
24        request = testing.DummyRequest()
25        inst = TutorialViews(request)
26        response = inst.hello()
27        self.assertEqual('Hello View', response['name'])
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
40        self.assertIn(b'<h1>Hi Home View', res.body)
41
42    def test_hello(self):
43        res = self.testapp.get('/howdy', status=200)
44        self.assertIn(b'<h1>Hi Hello View', res.body)
45
46    def test_hello_json(self):
47        res = self.testapp.get('/howdy.json', status=200)
48        self.assertIn(b'{"name": "Hello View"}', res.body)
49        self.assertEqual(res.content_type, 'application/json')
50

```

    
5.  Run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
.....
5 passed in 0.47 seconds

```

    
6.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
7.  Open [http://localhost:6543/howdy.json](http://localhost:6543/howdy.json) in your browser and you will see the resulting JSON response.
    

Analysis
---------------------------------------------

Earlier we changed our view functions and methods to return Python data. This change to a data-oriented view layer made test writing easier, decoupling the templating from the view logic.

Since Pyramid has a JSON renderer as well as the templating renderers, it is an easy step to return JSON. In this case we kept the exact same view and arranged to return a JSON encoding of the view data. We did this by:

*   Adding a route to map `/howdy.json` to a route name.
    
*   Providing a `@view_config` that associated that route name with an existing view.
    
*   _Overriding_ the view defaults in the view config that mentions the `hello_json` route, so that when the route is matched, we use the JSON renderer rather than the `home.pt` template renderer that would otherwise be used.
    

In fact, for pure AJAX-style web applications, we could re-use the existing route by using Pyramid's view predicates to match on the `Accepts:` header sent by modern AJAX implementations.

Pyramid's JSON renderer uses the base Python JSON encoder, thus inheriting its strengths and weaknesses. For example, Python can't natively JSON encode DateTime objects. There are a number of solutions for this in Pyramid, including extending the JSON renderer with a custom renderer.