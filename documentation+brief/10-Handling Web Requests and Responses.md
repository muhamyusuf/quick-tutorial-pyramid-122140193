# 10: Handling Web Requests and Responses — The Pyramid Web Framework v2.0.2
Web applications handle incoming requests and return outgoing responses. Pyramid makes working with requests and responses convenient and reliable.

Objectives
-------------------------------------------------

*   Learn the background on Pyramid's choices for requests and responses.
    
*   Grab data out of the request.
    
*   Change information in the response headers.
    

Background
-------------------------------------------------

Developing for the web means processing web requests. As this is a critical part of a web application, web developers need a robust, mature set of software for web requests and returning web responses.

Pyramid has always fit nicely into the existing world of Python web development (virtual environments, packaging, cookiecutters, first to embrace Python 3, and so on). Pyramid turned to the well-regarded [WebOb](about:blank/glossary.html#term-WebOb) Python library for request and response handling. In our example above, Pyramid hands `hello_world` a `request` that is [based on WebOb](about:blank/narr/webob.html#webob-chapter).

Steps
---------------------------------------

1.  First we copy the results of the `view_classes` step:
    
    ```
cd ..; cp -r view_classes request_response; cd request_response
$VENV/bin/pip install -e .

```

    
2.  Simplify the routes in `request_response/tutorial/__init__.py`:
    
    ```
1from pyramid.config import Configurator
2
3
4def main(global_config, **settings):
5    config = Configurator(settings=settings)
6    config.add_route('home', '/')
7    config.add_route('plain', '/plain')
8    config.scan('.views')
9    return config.make_wsgi_app()

```

    
3.  We only need one view in `request_response/tutorial/views.py`:
    
    ```
 1from pyramid.httpexceptions import HTTPFound
 2from pyramid.response import Response
 3from pyramid.view import view_config
 4
 5
 6class TutorialViews:
 7    def __init__(self, request):
 8        self.request = request
 9
10    @view_config(route_name='home')
11    def home(self):
12        return HTTPFound(location='/plain')
13
14    @view_config(route_name='plain')
15    def plain(self):
16        name = self.request.params.get('name', 'No Name Provided')
17
18        body = 'URL %s with name: %s' % (self.request.url, name)
19        return Response(
20            content_type='text/plain',
21            body=body
22        )

```

    
4.  Update the tests in `request_response/tutorial/tests.py`:
    
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
19        self.assertEqual(response.status, '302 Found')
20
21    def test_plain_without_name(self):
22        from .views import TutorialViews
23
24        request = testing.DummyRequest()
25        inst = TutorialViews(request)
26        response = inst.plain()
27        self.assertIn(b'No Name Provided', response.body)
28
29    def test_plain_with_name(self):
30        from .views import TutorialViews
31
32        request = testing.DummyRequest()
33        request.GET['name'] = 'Jane Doe'
34        inst = TutorialViews(request)
35        response = inst.plain()
36        self.assertIn(b'Jane Doe', response.body)
37
38
39class TutorialFunctionalTests(unittest.TestCase):
40    def setUp(self):
41        from tutorial import main
42
43        app = main({})
44        from webtest import TestApp
45
46        self.testapp = TestApp(app)
47
48    def test_plain_without_name(self):
49        res = self.testapp.get('/plain', status=200)
50        self.assertIn(b'No Name Provided', res.body)
51
52    def test_plain_with_name(self):
53        res = self.testapp.get('/plain?name=Jane%20Doe', status=200)
54        self.assertIn(b'Jane Doe', res.body)

```

    
5.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
.....
5 passed in 0.30 seconds

```

    
6.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
7.  Open [http://localhost:6543/](http://localhost:6543/) in your browser. You will be redirected to [http://localhost:6543/plain](http://localhost:6543/plain).
    
8.  Open [http://localhost:6543/plain?name=alice](http://localhost:6543/plain?name=alice) in your browser.
    

Analysis
---------------------------------------------

In this view class, we have two routes and two views, with the first leading to the second by an HTTP redirect. Pyramid can [generate redirects](about:blank/narr/views.html#http-redirect) by returning a special object from a view or raising a special exception.

In this Pyramid view, we get the URL being visited from `request.url`. Also, if you visited [http://localhost:6543/plain?name=alice](http://localhost:6543/plain?name=alice), the name is included in the body of the response:

```
URL http://localhost:6543/plain?name=alice with name: alice

```


Finally, we set the response's content type and body, then return the response.

We updated the unit and functional tests to prove that our code does the redirection, but also handles sending and not sending `/plain?name`.