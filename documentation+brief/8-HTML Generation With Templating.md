# 08: HTML Generation With Templating — The Pyramid Web Framework v2.0.2
Most web frameworks don't embed HTML in programming code. Instead, they pass data into a templating system. In this step we look at the basics of using HTML templates in Pyramid.

Background
-------------------------------------------------

Ouch. We have been making our own `Response` and filling the response body with HTML. You usually won't embed an HTML string directly in Python, but instead will use a templating language.

Pyramid doesn't mandate a particular database system, form library, and so on. It encourages replaceability. This applies equally to templating, which is fortunate: developers have strong views about template languages. As of Pyramid 1.5a2, Pyramid doesn't even bundle a template language!

It does, however, have strong ties to Jinja2, Mako, and Chameleon. In this step we see how to add [pyramid\_chameleon](https://github.com/Pylons/pyramid_chameleon) to your project, then change your views to use templating.

Objectives
-------------------------------------------------

*   Enable the `pyramid_chameleon` Pyramid add-on.
    
*   Generate HTML from template files.
    
*   Connect the templates as "renderers" for view code.
    
*   Change the view code to simply return data.
    

Steps
---------------------------------------

1.  Let's begin by using the previous package as a starting point for a new project:
    
    ```
cd ..; cp -r views templating; cd templating

```

    
2.  This step depends on `pyramid_chameleon`, so add it as a dependency in `templating/setup.py`:
    
    ```
 1from setuptools import setup
 2
 3# List of dependencies installed via `pip install -e .`
 4# by virtue of the Setuptools `install_requires` value below.
 5requires = [
 6    'pyramid',
 7    'pyramid_chameleon',
 8    'waitress',
 9]
10
11# List of dependencies installed via `pip install -e ".[dev]"`
12# by virtue of the Setuptools `extras_require` value in the Python
13# dictionary below.
14dev_requires = [
15    'pyramid_debugtoolbar',
16    'pytest',
17    'webtest',
18]
19
20setup(
21    name='tutorial',
22    install_requires=requires,
23    extras_require={
24        'dev': dev_requires,
25    },
26    entry_points={
27        'paste.app_factory': [
28            'main = tutorial:main'
29        ],
30    },
31)

```

    
3.  Now we can activate the development-mode distribution:
    
    ```
$VENV/bin/pip install -e .

```

    
4.  We need to connect `pyramid_chameleon` as a renderer by making a call in the setup of `templating/tutorial/__init__.py`:
    
    ```
 1from pyramid.config import Configurator
 2
 3
 4def main(global_config, **settings):
 5    config = Configurator(settings=settings)
 6    config.include('pyramid_chameleon')
 7    config.add_route('home', '/')
 8    config.add_route('hello', '/howdy')
 9    config.scan('.views')
10    return config.make_wsgi_app()

```

    
5.  Our `templating/tutorial/views.py` no longer has HTML in it:
    
    ```
 1from pyramid.view import view_config
 2
 3
 4# First view, available at http://localhost:6543/
 5@view_config(route_name='home', renderer='home.pt')
 6def home(request):
 7    return {'name': 'Home View'}
 8
 9
10# /howdy
11@view_config(route_name='hello', renderer='home.pt')
12def hello(request):
13    return {'name': 'Hello View'}

```

    
6.  Instead we have `templating/tutorial/home.pt` as a template:
    
    ```
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${name}</title>
</head>
<body>
<h1>Hi ${name}</h1>
</body>
</html>

```

    
7.  For convenience, change `templating/development.ini` to reload templates automatically with `pyramid.reload_templates`:
    
    ```
[app:main]
use = egg:tutorial
pyramid.reload_templates = true
pyramid.includes =
    pyramid_debugtoolbar

[server:main]
use = egg:waitress#main
listen = localhost:6543

```

    
8.  Our unit tests in `templating/tutorial/tests.py` can focus on data:
    
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
18        # Our view now returns data
19        self.assertEqual('Home View', response['name'])
20
21    def test_hello(self):
22        from .views import hello
23
24        request = testing.DummyRequest()
25        response = hello(request)
26        # Our view now returns data
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

    
9.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
....
4 passed in 0.46 seconds

```

    
10.  Run your Pyramid application with:
     
     ```
$VENV/bin/pserve development.ini --reload

```

     
11.  Open [http://localhost:6543/](http://localhost:6543/) and [http://localhost:6543/howdy](http://localhost:6543/howdy) in your browser.
     

Analysis
---------------------------------------------

Ahh, that looks better. We have a view that is focused on Python code. Our `@view_config` decorator specifies a [renderer](about:blank/glossary.html#term-renderer) that points to our template file. Our view then simply returns data which is then supplied to our template. Note that we used the same template for both views.

Note the effect on testing. We can focus on having a data-oriented contract with our view code.