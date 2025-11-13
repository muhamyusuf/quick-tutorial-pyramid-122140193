# 16: Collecting Application Info With Logging — The Pyramid Web Framework v2.0.2
Capture debugging and error output from your web applications using standard Python logging.

Background
-------------------------------------------------

It's important to know what is going on inside our web application. In development we might need to collect some output. In production, we might need to detect problems when other people use the site. We need _logging_.

Fortunately Pyramid uses the normal Python approach to logging. The project generated in your `development.ini` has a number of lines that configure the logging for you to some reasonable defaults. You then see messages sent by Pyramid, for example, when a new request comes in.

Objectives
-------------------------------------------------

*   Inspect the configuration setup used for logging.
    
*   Add logging statements to your view code.
    

Steps
---------------------------------------

1.  First we copy the results of the `view_classes` step:
    
    ```
cd ..; cp -r view_classes logging; cd logging
$VENV/bin/pip install -e .

```

    
2.  Extend `logging/tutorial/views.py` to log a message:
    
    ```
 1import logging
 2log = logging.getLogger(__name__)
 3
 4from pyramid.view import (
 5    view_config,
 6    view_defaults
 7    )
 8
 9
10@view_defaults(renderer='home.pt')
11class TutorialViews:
12    def __init__(self, request):
13        self.request = request
14
15    @view_config(route_name='home')
16    def home(self):
17        log.debug('In home view')
18        return {'name': 'Home View'}
19
20    @view_config(route_name='hello')
21    def hello(self):
22        log.debug('In hello view')
23        return {'name': 'Hello View'}

```

    
3.  Finally let's edit `development.ini` configuration file to enable logging for our Pyramid application:
    
    ```
[app:main]
use = egg:tutorial
pyramid.reload_templates = true
pyramid.includes =
    pyramid_debugtoolbar

[server:main]
use = egg:waitress#main
listen = localhost:6543

# Begin logging configuration

[loggers]
keys = root, tutorial

[logger_tutorial]
level = DEBUG
handlers =
qualname = tutorial

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = INFO
handlers = console

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration

```

    
4.  Make sure the tests still pass:
    
    ```
$VENV/bin/pytest tutorial/tests.py -q
....
4 passed in 0.41 seconds

```

    
5.  Run your Pyramid application with:
    
    ```
$VENV/bin/pserve development.ini --reload

```

    
6.  Open [http://localhost:6543/](http://localhost:6543/) and [http://localhost:6543/howdy](http://localhost:6543/howdy) in your browser. Note, both in the console and in the debug toolbar, the message that you logged.
    

Analysis
---------------------------------------------

In our configuration file `development.ini`, our `tutorial` Python package is set up as a logger and configured to log messages at a `DEBUG` or higher level. When you visit [http://localhost:6543](http://localhost:6543/), your console will now show:

```
2013-08-09 10:42:42,968 DEBUG [tutorial.views][MainThread] In home view

```


Also, if you have configured your Pyramid application to use the `pyramid_debugtoolbar`, logging statements appear in one of its menus.