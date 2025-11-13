# 03: Application Configuration with .ini Files — The Pyramid Web Framework v2.0.2
Use Pyramid's `pserve` command with a `.ini` configuration file for simpler, better application running.

Background
-------------------------------------------------

Pyramid has a first-class concept of [configuration](about:blank/narr/configuration.html#configuration-narr) distinct from code. This approach is optional, but its presence makes it distinct from other Python web frameworks. It taps into Python's [Setuptools](about:blank/glossary.html#term-Setuptools) library, which establishes conventions for installing and providing "[entry point](about:blank/glossary.html#term-entry-point)s" for Python projects. Pyramid uses an [entry point](about:blank/glossary.html#term-entry-point) to let a Pyramid application know where to find the WSGI app.

Objectives
-------------------------------------------------

*   Modify our `setup.py` to have an [entry point](about:blank/glossary.html#term-entry-point) telling Pyramid the location of the WSGI app.
    
*   Create an application driven by an `.ini` file.
    
*   Start the application with Pyramid's `pserve` command.
    
*   Move code into the package's `__init__.py`.
    

Steps
---------------------------------------

1.  First we copy the results of the previous step:
    
    ```
cd ..; cp -r package ini; cd ini

```

    
2.  Our `ini/setup.py` needs a [Setuptools](about:blank/glossary.html#term-Setuptools) [entry point](about:blank/glossary.html#term-entry-point) in the `setup()` function:
    
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
10setup(
11    name='tutorial',
12    install_requires=requires,
13    entry_points={
14        'paste.app_factory': [
15            'main = tutorial:main'
16        ],
17    },
18)

```

    
3.  We can now install our project, thus generating (or re-generating) an "egg" at `ini/tutorial.egg-info`:
    
    ```
$VENV/bin/pip install -e .

```

    
4.  Let's make a file `ini/development.ini` for our configuration:
    
    ```
1[app:main]
2use = egg:tutorial
3
4[server:main]
5use = egg:waitress#main
6listen = localhost:6543

```

    
5.  We can refactor our startup code from the previous step's `app.py` into `ini/tutorial/__init__.py`:
    
    ```
 1from pyramid.config import Configurator
 2from pyramid.response import Response
 3
 4
 5def hello_world(request):
 6    return Response('<body><h1>Hello World!</h1></body>')
 7
 8
 9def main(global_config, **settings):
10    config = Configurator(settings=settings)
11    config.add_route('hello', '/')
12    config.add_view(hello_world, route_name='hello')
13    return config.make_wsgi_app()

```

    
6.  Now that `ini/tutorial/app.py` isn't used, let's remove it:
    
7.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
8.  Open [http://localhost:6543/](http://localhost:6543/).
    

Analysis
---------------------------------------------

Our `development.ini` file is read by `pserve` and serves to bootstrap our application. Processing then proceeds as described in the Pyramid chapter on [application startup](about:blank/narr/startup.html#startup-chapter):

*   `pserve` looks for `[app:main]` and finds `use = egg:tutorial`.
    
*   The projects's `setup.py` has defined an [entry point](about:blank/glossary.html#term-entry-point) (lines 10-13) for the project's "main" [entry point](about:blank/glossary.html#term-entry-point) of `tutorial:main`.
    
*   The `tutorial` package's `__init__` has a `main` function.
    
*   This function is invoked, with the values from certain `.ini` sections passed in.
    

The `.ini` file is also used for two other functions:

*   _Configuring the WSGI server_. `[server:main]` wires up the choice of which WSGI _server_ for your WSGI _application_. In this case, we are using `waitress` which we specified in `tutorial/setup.py` and was installed in the [Requirements](requirements.html) step at the start of this tutorial. It also wires up the _port number_: `listen = localhost:6543` tells `waitress` to listen on host `localhost` at port `6543`.
    
    Note
    
    Running the command `$VENV/bin/pip install -e .` will check for previously installed packages in our virtual environment that are specified in our package's `setup.py` file, then install our package in editable mode, installing any requirements that were not previously installed. If a requirement was manually installed previously on the command line or otherwise, in this case Waitress, then `$VENV/bin/pip install -e .` will merely check that it is installed and move on.
    
*   _Configuring Python logging_. Pyramid uses Python standard logging, which needs a number of configuration values. The `.ini` serves this function. This provides the console log output that you see on startup and each request.
    

We moved our startup code from `app.py` to the package's `tutorial/__init__.py`. This isn't necessary, but it is a common style in Pyramid to take the WSGI app bootstrapping out of your module's code and put it in the package's `__init__.py`.

The `pserve` application runner has a number of command-line arguments and options. We are using `--reload` which tells `pserve` to watch the filesystem for changes to relevant code (Python files, the INI file, etc.) and, when something changes, restart the application. Very handy during development.