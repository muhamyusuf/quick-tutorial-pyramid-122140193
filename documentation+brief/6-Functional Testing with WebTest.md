# 06: Functional Testing with WebTest — The Pyramid Web Framework v2.0.2
Write end-to-end full-stack testing using `webtest`.

Background
-------------------------------------------------

Unit tests are a common and popular approach to test-driven development (TDD). In web applications, though, the templating and entire apparatus of a web site are important parts of the delivered quality. We'd like a way to test these.

[WebTest](https://docs.pylonsproject.org/projects/webtest/en/latest/) is a Python package that does functional testing. With WebTest you can write tests which simulate a full HTTP request against a WSGI application, then test the information in the response. For speed purposes, WebTest skips the setup/teardown of an actual HTTP server, providing tests that run fast enough to be part of TDD.

Objectives
-------------------------------------------------

*   Write a test which checks the contents of the returned HTML.
    

Steps
---------------------------------------

1.  First we copy the results of the previous step.
    
    ```
cd ..; cp -r unit_testing functional_testing; cd functional_testing

```

    
2.  Add `webtest` to our project's dependencies in `setup.py` as a [Setuptools](about:blank/glossary.html#term-Setuptools) "extra":
    
    ```
 1from setuptools import setup
 2
 3# List of dependencies installed via `pip install -e .`
 4# by virtue of the Setuptools `install_requires` value below.
 5requires = [
 6    'pyramid',
 7    'waitress',
 8]
 9
10# List of dependencies installed via `pip install -e ".[dev]"`
11# by virtue of the Setuptools `extras_require` value in the Python
12# dictionary below.
13dev_requires = [
14    'pyramid_debugtoolbar',
15    'pytest',
16    'webtest',
17]
18
19setup(
20    name='tutorial',
21    install_requires=requires,
22    extras_require={
23        'dev': dev_requires,
24    },
25    entry_points={
26        'paste.app_factory': [
27            'main = tutorial:main'
28        ],
29    },
30)

```

    
3.  Install our project and its newly added dependency. Note that we use the extra specifier `[dev]` to install testing requirements for development and surround it and the period with double quote marks.
    
    ```
$VENV/bin/pip install -e ".[dev]"

```

    
4.  Let's extend `functional_testing/tutorial/tests.py` to include a functional test:
    
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
13    def test_hello_world(self):
14        from tutorial import hello_world
15
16        request = testing.DummyRequest()
17        response = hello_world(request)
18        self.assertEqual(response.status_code, 200)
19
20
21class TutorialFunctionalTests(unittest.TestCase):
22    def setUp(self):
23        from tutorial import main
24        app = main({})
25        from webtest import TestApp
26
27        self.testapp = TestApp(app)
28
29    def test_hello_world(self):
30        res = self.testapp.get('/', status=200)
31        self.assertIn(b'<h1>Hello World!</h1>', res.body)

```

    
    Be sure this file is not executable, or `pytest` may not include your tests.
    
5.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
..
2 passed in 0.25 seconds

```

    

Analysis
---------------------------------------------

We now have the end-to-end testing we were looking for. WebTest lets us simply extend our existing `pytest`\-based test approach with functional tests that are reported in the same output. These new tests not only cover our templating, but they didn't dramatically increase the execution time of our tests.