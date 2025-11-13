# Requirements — The Pyramid Web Framework v2.0.2
Let's get our tutorial environment set up. Most of the set up work is in standard Python development practices (install Python and make an isolated virtual environment.)

Note

Pyramid encourages standard Python development practices with packaging tools, virtual environments, logging, and so on. There are many variations, implementations, and opinions across the Python community. For consistency, ease of documentation maintenance, and to minimize confusion, the Pyramid _documentation_ has adopted specific conventions that are consistent with the [Python Packaging Authority](about:blank/glossary.html#term-Python-Packaging-Authority).

This _Quick Tutorial_ is based on:

*   **Python 3.8**. Pyramid fully supports Python 3.6+. This tutorial uses **Python 3.8**.
    
*   **venv**. We believe in virtual environments. For this tutorial, we use Python 3's built-in solution [venv](about:blank/glossary.html#term-venv).
    
*   **pip**. We use [pip](about:blank/glossary.html#term-pip) for package management.
    
*   **Workspaces, projects, and packages.** Our home directory will contain a _tutorial workspace_ with our Python virtual environment and _Python projects_ (a directory with packaging information and _Python packages_ of working code.)
    
*   **Unix commands**. Commands in this tutorial use Unix syntax and paths. Windows users should adjust commands accordingly.
    

Note

Pyramid was one of the first web frameworks to fully support Python 3 in October 2011.

Note

Windows commands use the plain old MSDOS shell. For PowerShell command syntax, see its documentation.

Steps
---------------------------------------

1.  [Install Python 3](#install-python-3)
    
2.  [Create a project directory structure](#create-a-project-directory-structure)
    
3.  [Set an environment variable](#set-an-environment-variable)
    
4.  [Create a virtual environment](#create-a-virtual-environment)
    
5.  [Install Pyramid](#install-pyramid)
    

### Install Python 3

See the detailed recommendation for your operating system described under [Installing Pyramid](about:blank/narr/install.html#installing-chapter).

*   [For macOS Users](about:blank/narr/install.html#for-macos-users)
    
*   [If You Don't Yet Have a Python Interpreter (Unix)](about:blank/narr/install.html#if-you-don-t-yet-have-a-python-interpreter-unix)
    
*   [If You Don't Yet Have a Python Interpreter (Windows)](about:blank/narr/install.html#if-you-don-t-yet-have-a-python-interpreter-windows)
    

### Create a project directory structure

We will arrive at a directory structure of `workspace -> project -> package`, where our workspace is named `quick_tutorial`. The following tree diagram shows how this will be structured, and where our [virtual environment](about:blank/glossary.html#term-virtual-environment) will reside as we proceed through the tutorial:

```
~
└── projects
    └── quick_tutorial
        ├── env
        └── step_one
            ├── intro
            │   ├── __init__.py
            │   └── app.py
            └── setup.py

```


For macOS and Linux, the commands to do so are as follows:

```
# macOS and Linux
cd ~
mkdir -p projects/quick_tutorial
cd projects/quick_tutorial

```


For Windows:

```
# Windows
cd \
mkdir projects\quick_tutorial
cd projects\quick_tutorial

```


In the above figure, your user home directory is represented by `~`. In your home directory, all of your projects are in the `projects` directory. This is a general convention not specific to Pyramid that many developers use. Windows users will do well to use `c:\` as the location for `projects` in order to avoid spaces in any of the path names.

Next within `projects` is your workspace directory, here named `quick_tutorial`. A workspace is a common term used by integrated development environments (IDE), like PyCharm and PyDev, where virtual environments, specific project files, and repositories are stored.

### Set an environment variable

This tutorial will refer frequently to the location of the [virtual environment](about:blank/glossary.html#term-virtual-environment). We set an environment variable to save typing later.

```
# macOS and Linux
export VENV=~/projects/quick_tutorial/env

```


```
# Windows
set VENV=c:\projects\quick_tutorial\env

```


### Create a virtual environment

`venv` is a tool to create isolated Python 3 environments, each with its own Python binary and independent set of installed Python packages in its site directories. Let's create one, using the location we just specified in the environment variable.

```
# macOS and Linux
python3 -m venv $VENV

```


```
# Windows
python -m venv %VENV%

```


### Update packaging tools in the virtual environment

It's always a good idea to update to the very latest version of packaging tools because the installed Python bundles only the version that was available at the time of its release.

```
# macOS and Linux
$VENV/bin/pip install --upgrade pip setuptools

```


```
# Windows
%VENV%\Scripts\pip install --upgrade pip setuptools

```


### Install Pyramid

We have our Python standard prerequisites out of the way. The Pyramid part is pretty easy. We'll also install a WSGI server, Waitress.

```
# macOS and Linux
$VENV/bin/pip install "pyramid==2.0.2" waitress

# Windows
%VENV%\Scripts\pip install "pyramid==2.0.2" waitress
```


Our Python virtual environment now has the Pyramid software available as well as the `waitress` package.