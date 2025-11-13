# 05: Unit Tests and pytest — The Pyramid Web Framework v2.0.2
Provide unit testing for our project's Python code.

Background
-------------------------------------------------

As the mantra says, "Untested code is broken code." The Python community has had a long culture of writing test scripts which ensure that your code works correctly as you write it and maintain it in the future. Pyramid has always had a deep commitment to testing, with 100% test coverage from the earliest pre-releases.

Python includes a [unit testing framework](https://docs.python.org/3/library/unittest.html#unittest-minimal-example "(in Python v3.11)") in its standard library. Over the years a number of Python projects, such as [pytest](https://docs.pytest.org/en/latest/index.html#features "(in pytest v8.0.0.dev250+g7500fe4)"), have extended this framework with alternative test runners that provide more convenience and functionality. The Pyramid developers use `pytest`, which we'll use in this tutorial.

Don't worry, this tutorial won't be pedantic about "test-driven development" (TDD). We'll do just enough to ensure that, in each step, we haven't majorly broken the code. As you're writing your code, you might find this more convenient than changing to your browser constantly and clicking reload.

We'll also leave discussion of [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) for another section.

Objectives
-------------------------------------------------

*   Write unit tests that ensure the quality of our code.
    
*   Install a Python package (`pytest`) which helps in our testing.
    

Steps
---------------------------------------

1.  First we copy the results of the previous step.
    
    ```
cd ..; cp -r debugtoolbar unit_testing; cd unit_testing

```

    
2.  Add `pytest` to our project's dependencies in `setup.py` as a [Setuptools](about:blank/glossary.html#term-Setuptools) "extra":
    
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
16]
17
18setup(
19    name='tutorial',
20    install_requires=requires,
21    extras_require={
22        'dev': dev_requires,
23    },
24    entry_points={
25        'paste.app_factory': [
26            'main = tutorial:main'
27        ],
28    },
29)

```

    
3.  Install our project and its newly added dependency. Note that we use the extra specifier `[dev]` to install testing requirements for development and surround it and the period with double quote marks.
    
    ```
$VENV/bin/pip install -e ".[dev]"

```

    
4.  Now we write a simple unit test in `unit_testing/tutorial/tests.py`:
    
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

```

    
5.  Now run the tests:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
.
1 passed in 0.14 seconds

```

    

Analysis
---------------------------------------------

Our `tests.py` imports the Python standard unit testing framework. To make writing Pyramid-oriented tests more convenient, Pyramid supplies some `pyramid.testing` helpers which we use in the test setup and teardown. Our one test imports the view, makes a dummy request, and sees if the view returns what we expect.

The `tests.TutorialViewTests.test_hello_world` test is a small example of a unit test. First, we import the view inside each test. Why not import at the top, like in normal Python code? Because imports can cause effects that break a test. We'd like our tests to be in _units_, hence the name _unit_ testing. Each test should isolate itself to the correct degree.

Our test then makes a fake incoming web request, then calls our Pyramid view. We test the HTTP status code on the response to make sure it matches our expectations.

Note that our use of `pyramid.testing.setUp()` and `pyramid.testing.tearDown()` aren't actually necessary here; they are only necessary when your test needs to make use of the `config` object (it's a Configurator) to add stuff to the configuration state before calling the view.