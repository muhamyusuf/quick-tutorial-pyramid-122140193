# 02: Python Packages for Pyramid Applications — The Pyramid Web Framework v2.0.2
Most modern Python development is done using Python packages, an approach Pyramid puts to good use. In this step we redo "Hello World" as a minimal Python package inside a minimal Python project.

Background
-------------------------------------------------

Python developers can organize a collection of modules and files into a namespaced unit called a [package](https://docs.python.org/3/tutorial/modules.html#tut-packages "(in Python v3.11)"). If a directory is on `sys.path` and has a special file named `__init__.py`, it is treated as a Python package.

Packages can be bundled up, made available for installation, and installed through a toolchain oriented around a `setup.py` file. For this tutorial, this is all you need to know:

*   We will have a directory for each tutorial step as a _project_.
    
*   This project will contain a `setup.py` which injects the features of the project machinery into the directory.
    
*   In this project we will make a `tutorial` subdirectory into a Python _package_ using an `__init__.py` Python module file.
    
*   We will run `pip install -e .` to install our project in development mode.
    

In summary:

*   You'll do your development in a Python _package_.
    
*   That package will be part of a _project_.
    

Objectives
-------------------------------------------------

*   Make a Python "package" directory with an `__init__.py`.
    
*   Get a minimum Python "project" in place by making a `setup.py`.
    
*   Install our `tutorial` project in development mode.
    

Steps
---------------------------------------

1.  Make an area for this tutorial step:
    
    ```
cd ..; mkdir package; cd package

```

    
2.  In `package/setup.py`, enter the following:
    
    ```
from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'waitress',
]

setup(
    name='tutorial',
    install_requires=requires,
)

```

    
3.  Make the new project installed for development then make a directory for the actual code:
    
    ```
$VENV/bin/pip install -e .
mkdir tutorial

```

    
4.  Enter the following into `package/tutorial/__init__.py`:
    
5.  Enter the following into `package/tutorial/app.py`:
    
    ```
from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)

```

    
6.  Run the WSGI application with:
    
    ```
$VENV/bin/python tutorial/app.py

```

    
7.  Open [http://localhost:6543/](http://localhost:6543/) in your browser.
    

Analysis
---------------------------------------------

Python packages give us an organized unit of project development. Python projects, via `setup.py`, give us special features when our package is installed (in this case, in local development mode, also called local editable mode as indicated by `-e .`).

In this step we have a Python package called `tutorial`. We use the same name in each step of the tutorial, to avoid unnecessary retyping.

Above this `tutorial` directory we have the files that handle the packaging of this project. At the moment, all we need is a bare-bones `setup.py`.

Everything else is the same about our application. We simply made a Python package with a `setup.py` and installed it in development mode.

Note that the way we're running the app (`python tutorial/app.py`) is a bit of an odd duck. We would never do this unless we were writing a tutorial that tries to capture how this stuff works one step at a time. It's generally a bad idea to run a Python module inside a package directly as a script.