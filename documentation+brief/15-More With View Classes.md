# 15: More With View Classes — The Pyramid Web Framework v2.0.2
Group views into a class, sharing configuration, state, and logic.

Background
-------------------------------------------------

As part of its mission to help build more ambitious web applications, Pyramid provides many more features for views and view classes.

The Pyramid documentation discusses views as a Python "callable". This callable can be a function, an object with a `__call__`, or a Python class. In this last case, methods on the class can be decorated with `@view_config` to register the class methods with the [configurator](about:blank/glossary.html#term-configurator) as a view.

At first, our views were simple, free-standing functions. Many times your views are related: different ways to look at or work on the same data, or a REST API that handles multiple operations. Grouping these together as a [view class](about:blank/narr/views.html#class-as-view) makes sense:

*   Group views.
    
*   Centralize some repetitive defaults.
    
*   Share some state and helpers.
    

Pyramid views have [view predicates](about:blank/narr/viewconfig.html#view-configuration-parameters) that determine which view is matched to a request, based on factors such as the request method, the form parameters, and so on. These predicates provide many axes of flexibility.

The following shows a simple example with four operations: view a home page which leads to a form, save a change, and press the delete button.

Objectives
-------------------------------------------------

*   Group related views into a view class.
    
*   Centralize configuration with class-level `@view_defaults`.
    
*   Dispatch one route/URL to multiple views based on request data.
    
*   Share states and logic between views and templates via the view class.
    

Steps
---------------------------------------

1.  First we copy the results of the `templating` step:
    
    ```
cd ..; cp -r templating more_view_classes; cd more_view_classes
$VENV/bin/pip install -e .

```

    
2.  Our route in `more_view_classes/tutorial/__init__.py` needs some replacement patterns:
    
    ```
 1from pyramid.config import Configurator
 2
 3
 4def main(global_config, **settings):
 5    config = Configurator(settings=settings)
 6    config.include('pyramid_chameleon')
 7    config.add_route('home', '/')
 8    config.add_route('hello', '/howdy/{first}/{last}')
 9    config.scan('.views')
10    return config.make_wsgi_app()

```

    
3.  Our `more_view_classes/tutorial/views.py` now has a view class with several views:
    
    ```
 1from pyramid.view import (
 2    view_config,
 3    view_defaults
 4    )
 5
 6
 7@view_defaults(route_name='hello')
 8class TutorialViews:
 9    def __init__(self, request):
10        self.request = request
11        self.view_name = 'TutorialViews'
12
13    @property
14    def full_name(self):
15        first = self.request.matchdict['first']
16        last = self.request.matchdict['last']
17        return first + ' ' + last
18
19    @view_config(route_name='home', renderer='home.pt')
20    def home(self):
21        return {'page_title': 'Home View'}
22
23    # Retrieving /howdy/first/last the first time
24    @view_config(renderer='hello.pt')
25    def hello(self):
26        return {'page_title': 'Hello View'}
27
28    # Posting to /howdy/first/last via the "Edit" submit button
29    @view_config(request_method='POST', renderer='edit.pt')
30    def edit(self):
31        new_name = self.request.params['new_name']
32        return {'page_title': 'Edit View', 'new_name': new_name}
33
34    # Posting to /howdy/first/last via the "Delete" submit button
35    @view_config(request_method='POST', request_param='form.delete',
36                 renderer='delete.pt')
37    def delete(self):
38        print ('Deleted')
39        return {'page_title': 'Delete View'}

```

    
4.  Our primary view needs a template at `more_view_classes/tutorial/home.pt`:
    
    ```
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${view.view_name} - ${page_title}</title>
</head>
<body>
<h1>${view.view_name} - ${page_title}</h1>

<p>Go to the <a href="${request.route_url('hello', first='jane',
        last='doe')}">form</a>.</p>
</body>
</html>

```

    
5.  Ditto for our other view from the previous section at `more_view_classes/tutorial/hello.pt`:
    
    ```
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${view.view_name} - ${page_title}</title>
</head>
<body>
<h1>${view.view_name} - ${page_title}</h1>
<p>Welcome, ${view.full_name}</p>
<form method="POST"
      action="${request.current_route_url()}">
    <input name="new_name"/>
    <input type="submit" name="form.edit" value="Save"/>
    <input type="submit" name="form.delete" value="Delete"/>
</form>
</body>
</html>

```

    
6.  We have an edit view that also needs a template at `more_view_classes/tutorial/edit.pt`:
    
    ```
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${view.view_name} - ${page_title}</title>
</head>
<body>
<h1>${view.view_name} - ${page_title}</h1>
<p>You submitted <code>${new_name}</code></p>
</body>
</html>

```

    
7.  And finally the delete view's template at `more_view_classes/tutorial/delete.pt`:
    
    ```
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${page_title}</title>
</head>
<body>
<h1>${view.view_name} - ${page_title}</h1>
</body>
</html>

```

    
8.  Our tests in `more_view_classes/tutorial/tests.py` fail, so let's modify them:
    
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
19        self.assertEqual('Home View', response['page_title'])
20
21class TutorialFunctionalTests(unittest.TestCase):
22    def setUp(self):
23        from tutorial import main
24        app = main({})
25        from webtest import TestApp
26
27        self.testapp = TestApp(app)
28
29    def test_home(self):
30        res = self.testapp.get('/', status=200)
31        self.assertIn(b'TutorialViews - Home View', res.body)

```

    
9.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
..
2 passed in 0.40 seconds

```

    
10.  Run your Pyramid application with:
     
     ```
$VENV/bin/pserve development.ini --reload

```

     
11.  Open [http://localhost:6543/howdy/jane/doe](http://localhost:6543/howdy/jane/doe) in your browser. Click the `Save` and `Delete` buttons, and watch the output in the console window.
     

Analysis
---------------------------------------------

As you can see, the four views are logically grouped together. Specifically:

*   We have a `home` view available at [http://localhost:6543/](http://localhost:6543/) with a clickable link to the `hello` view.
    
*   The second view is returned when you go to `/howdy/jane/doe`. This URL is mapped to the `hello` route that we centrally set using the optional `@view_defaults`.
    
*   The third view is returned when the form is submitted with a `POST` method. This rule is specified in the `@view_config` for that view.
    
*   The fourth view is returned when clicking on a button such as `<input type="submit" name="form.delete" value="Delete"/>`.
    

In this step we show, using the following information as criteria, how to decide which view to use:

*   Method of the HTTP request (`GET`, `POST`, etc.)
    
*   Parameter information in the request (submitted form field names)
    

We also centralize part of the view configuration to the class level with `@view_defaults`, then in one view, override that default just for that one view. Finally, we put this commonality between views to work in the view class by sharing:

*   State assigned in `TutorialViews.__init__`
    
*   A computed value
    

These are then available both in the view methods and in the templates (e.g., `${view.view_name}` and `${view.full_name}`).

As a note, we made a switch in our templates on how we generate URLs. We previously hardcoded the URLs, such as:

```
<a href="/howdy/jane/doe">Howdy</a>

```


In `home.pt` we switched to:

```
<a href="${request.route_url('hello', first='jane',
    last='doe')}">form</a>

```


Pyramid has rich facilities to help generate URLs in a flexible, non-error prone fashion.