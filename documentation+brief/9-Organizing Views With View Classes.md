# 09: Organizing Views With View Classes — The Pyramid Web Framework v2.0.2
Change our view functions to be methods on a view class, then move some declarations to the class level.

Background
-------------------------------------------------

So far our views have been simple, free-standing functions. Many times your views are related to one another. They may consist of different ways to look at or work on the same data, or be a REST API that handles multiple operations. Grouping these views together as a [view class](about:blank/narr/views.html#class-as-view) makes sense:

*   Group views.
    
*   Centralize some repetitive defaults.
    
*   Share some state and helpers.
    

In this step we just do the absolute minimum to convert the existing views to a view class. In a later tutorial step, we'll examine view classes in depth.

Objectives
-------------------------------------------------

*   Group related views into a view class.
    
*   Centralize configuration with class-level `@view_defaults`.
    

Steps
---------------------------------------

1.  First we copy the results of the previous step:
    
    ```
cd ..; cp -r templating view_classes; cd view_classes
$VENV/bin/pip install -e .

```

    
2.  Our `view_classes/tutorial/views.py` now has a view class with our two views:
    
    ```
 1from pyramid.view import (
 2    view_config,
 3    view_defaults
 4    )
 5
 6@view_defaults(renderer='home.pt')
 7class TutorialViews:
 8    def __init__(self, request):
 9        self.request = request
10
11    @view_config(route_name='home')
12    def home(self):
13        return {'name': 'Home View'}
14
15    @view_config(route_name='hello')
16    def hello(self):
17        return {'name': 'Hello View'}

```

    
3.  Our unit tests in `view_classes/tutorial/tests.py` don't run, so let's modify them to import the view class, and make an instance before getting a response:
    
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

```

    
4.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
....
4 passed in 0.34 seconds

```

    
5.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
6.  Open [http://localhost:6543/](http://localhost:6543/) and [http://localhost:6543/howdy](http://localhost:6543/howdy) in your browser.
    

Analysis
---------------------------------------------

To ease the transition to view classes, we didn't introduce any new functionality. We simply changed the view functions to methods on a view class, then updated the tests.

In our `TutorialViews` view class, you can see that our two view functions are logically grouped together as methods on a common class. Since the two views shared the same template, we could move that to a `@view_defaults` decorator at the class level.

The tests needed to change. Obviously we needed to import the view class. But you can also see the pattern in the tests of instantiating the view class with the dummy request first, then calling the view method being tested.