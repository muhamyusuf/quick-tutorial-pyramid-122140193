# 04: Easier Development with debugtoolbar — The Pyramid Web Framework v2.0.2
Error handling and introspection using the `pyramid_debugtoolbar` add-on.

Background
-------------------------------------------------

As we introduce the basics, we also want to show how to be productive in development and debugging. For example, we just discussed template reloading, and earlier we showed `--reload` for application reloading.

`pyramid_debugtoolbar` is a popular Pyramid add-on which makes several tools available in your browser. Adding it to your project illustrates several points about configuration.

Objectives
-------------------------------------------------

*   Install and enable the toolbar to help during development.
    
*   Explain Pyramid add-ons.
    
*   Show how an add-on gets configured into your application.
    

Steps
---------------------------------------

1.  First we copy the results of the previous step.
    
    ```
cd ..; cp -r ini debugtoolbar; cd debugtoolbar

```

    
2.  Add `pyramid_debugtoolbar` to our project's dependencies in `setup.py` as a [Setuptools](about:blank/glossary.html#term-Setuptools) "extra" for development:
    
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
15]
16
17setup(
18    name='tutorial',
19    install_requires=requires,
20    extras_require={
21        'dev': dev_requires,
22    },
23    entry_points={
24        'paste.app_factory': [
25            'main = tutorial:main'
26        ],
27    },
28)

```

    
3.  Install our project and its newly added dependency. Note that we use the extra specifier `[dev]` to install development requirements and surround it and the period with double quote marks.
    
    ```
$VENV/bin/pip install -e ".[dev]"

```

    
4.  Our `debugtoolbar/development.ini` gets a configuration entry for `pyramid.includes`:
    
    ```
1[app:main]
2use = egg:tutorial
3pyramid.includes =
4    pyramid_debugtoolbar
5
6[server:main]
7use = egg:waitress#main
8listen = localhost:6543

```

    
5.  Run the WSGI application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
6.  Open [http://localhost:6543/](http://localhost:6543/) in your browser. See the handy toolbar on the right.
    

Analysis
---------------------------------------------

`pyramid_debugtoolbar` is a full-fledged Python package, available on PyPI just like thousands of other Python packages. Thus we start by installing the `pyramid_debugtoolbar` package into our virtual environment using normal Python package installation commands.

The `pyramid_debugtoolbar` Python package is also a Pyramid add-on, which means we need to include its add-on configuration into our web application. We could do this with imperative configuration in `tutorial/__init__.py` by using `config.include`. Pyramid also supports wiring in add-on configuration via our `development.ini` using `pyramid.includes`. We use this to load the configuration for the debugtoolbar.

You'll now see an attractive button on the right side of your browser, which you may click to provide introspective access to debugging information in a new browser tab. Even better, if your web application generates an error, you will see a nice traceback on the screen. When you want to disable this toolbar, there's no need to change code: you can remove it from `pyramid.includes` in the relevant `.ini` configuration file (thus showing why configuration files are handy).

Note that the toolbar injects a small amount of HTML/CSS into your app just before the closing `</body>` tag in order to display itself. If you start to experience otherwise inexplicable client-side weirdness, you can shut it off by commenting out the `pyramid_debugtoolbar` line in `pyramid.includes` temporarily.

Finally we've introduced the concept of [Setuptools](about:blank/glossary.html#term-Setuptools) extras. These are optional or recommended features that may be installed with an "extras" specifier, in this case, `dev`. The specifier is the name of a key in a Python dictionary, and is surrounded by square brackets when invoked on the command line, for example, . The value for the key is a Python list of dependencies.