# 12: Templating With jinja2 — The Pyramid Web Framework v2.0.2
We just said Pyramid doesn't prefer one templating language over another. Time to prove it. Jinja2 is a popular templating system, used in Flask and modeled after Django's templates. Let's add `pyramid_jinja2`, a Pyramid [add-on](about:blank/glossary.html#term-add-on) which enables Jinja2 as a [renderer](about:blank/glossary.html#term-renderer) in our Pyramid applications.

Objectives
-------------------------------------------------

*   Show Pyramid's support for different templating systems.
    
*   Learn about installing Pyramid add-ons.
    

Steps
---------------------------------------

1.  In this step let's start by copying the `view_class` step's directory from a few steps ago.
    
    ```
cd ..; cp -r view_classes jinja2; cd jinja2

```

    
2.  Add `pyramid_jinja2` to our project's dependencies in `setup.py`:
    
    ```
 1from setuptools import setup
 2
 3# List of dependencies installed via `pip install -e .`
 4# by virtue of the Setuptools `install_requires` value below.
 5requires = [
 6    'pyramid',
 7    'pyramid_chameleon',
 8    'pyramid_jinja2',
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

    
3.  Install our project and its newly added dependency.
    
    ```
$VENV/bin/pip install -e .

```

    
4.  We need to include `pyramid_jinja2` in `jinja2/tutorial/__init__.py`:
    
    ```
 1from pyramid.config import Configurator
 2
 3
 4def main(global_config, **settings):
 5    config = Configurator(settings=settings)
 6    config.include('pyramid_jinja2')
 7    config.add_route('home', '/')
 8    config.add_route('hello', '/howdy')
 9    config.scan('.views')
10    return config.make_wsgi_app()

```

    
5.  Our `jinja2/tutorial/views.py` simply changes its `renderer`:
    
    ```
 1from pyramid.view import (
 2    view_config,
 3    view_defaults
 4    )
 5
 6
 7@view_defaults(renderer='home.jinja2')
 8class TutorialViews:
 9    def __init__(self, request):
10        self.request = request
11
12    @view_config(route_name='home')
13    def home(self):
14        return {'name': 'Home View'}
15
16    @view_config(route_name='hello')
17    def hello(self):
18        return {'name': 'Hello View'}

```

    
6.  Add `jinja2/tutorial/home.jinja2` as a template:
    
    ```
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: {{ name }}</title>
</head>
<body>
<h1>Hi {{ name }}</h1>
</body>
</html>

```

    
7.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
....
4 passed in 0.40 seconds

```

    
8.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
9.  Open [http://localhost:6543/](http://localhost:6543/) in your browser.
    

Analysis
---------------------------------------------

Getting a Pyramid add-on into Pyramid is simple. First you use normal Python package installation tools to install the add-on package into your Python virtual environment. You then tell Pyramid's configurator to run the setup code in the add-on. In this case the setup code told Pyramid to make a new "renderer" available that looked for `.jinja2` file extensions.

Our view code stayed largely the same. We simply changed the file extension on the renderer. For the template, the syntax for Chameleon and Jinja2's basic variable insertion is very similar.