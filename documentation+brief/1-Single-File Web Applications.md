# 01: Single-File Web Applications — The Pyramid Web Framework v2.0.2
What's the simplest way to get started in Pyramid? A single-file module. No Python packages, no `pip install -e .`, no other machinery.

Background
-------------------------------------------------

Microframeworks were all the rage, until the next shiny thing came along. "Microframework" is a marketing term, not a technical one. They have a low mental overhead: they do so little, the only things you have to worry about are _your things_.

Pyramid is special because it can act as a single-file module microframework. You can have a single Python file that can be executed directly by Python. But Pyramid also provides facilities to scale to the largest of applications.

Python has a standard called [WSGI](about:blank/glossary.html#term-WSGI) that defines how Python web applications plug into standard servers, getting passed incoming requests, and returning responses. Most modern Python web frameworks obey an "MVC" (model-view-controller) application pattern, where the data in the model has a view that mediates interaction with outside systems.

In this step we'll see a brief glimpse of WSGI servers, WSGI applications, requests, responses, and views.

Objectives
-------------------------------------------------

*   Get a running Pyramid web application, as simply as possible.
    
*   Use that as a well-understood base for adding each unit of complexity.
    
*   Initial exposure to WSGI apps, requests, views, and responses.
    

Steps
---------------------------------------

1.  Make sure you have followed the steps in [Requirements](requirements.html).
    
2.  Starting from your workspace directory (`~/projects/quick_tutorial`), create a directory for this step:
    
    ```
cd ~/projects/quick_tutorial; mkdir hello_world; cd hello_world

```

    
3.  Copy the following into `hello_world/app.py`:
    
    ```
 1from waitress import serve
 2from pyramid.config import Configurator
 3from pyramid.response import Response
 4
 5
 6def hello_world(request):
 7    print('Incoming request')
 8    return Response('<body><h1>Hello World!</h1></body>')
 9
10
11if __name__ == '__main__':
12    with Configurator() as config:
13        config.add_route('hello', '/')
14        config.add_view(hello_world, route_name='hello')
15        app = config.make_wsgi_app()
16    serve(app, host='0.0.0.0', port=6543)

```

    
4.  Run the application:
    
5.  Open [http://localhost:6543/](http://localhost:6543/) in your browser.
    

Analysis
---------------------------------------------

New to Python web programming? If so, some lines in the module merit explanation:

1.  _Line 11_. The `if __name__ == '__main__':` is Python's way of saying, "Start here when running from the command line", rather than when this module is imported.
    
2.  _Lines 12-14_. Use Pyramid's [configurator](about:blank/glossary.html#term-configurator) in a [context manager](about:blank/glossary.html#term-context-manager) to connect [view](about:blank/glossary.html#term-view) code to a particular URL [route](about:blank/glossary.html#term-route).
    
3.  _Lines 6-8_. Implement the view code that generates the [response](about:blank/glossary.html#term-response).
    
4.  _Lines 15-17_. Publish a [WSGI](about:blank/glossary.html#term-WSGI) app using an HTTP server.
    

As shown in this example, the [configurator](about:blank/glossary.html#term-configurator) plays a central role in Pyramid development. Building an application from loosely-coupled parts via [Application Configuration](about:blank/narr/configuration.html#configuration-narr) is a central idea in Pyramid, one that we will revisit regularly in this _Quick Tutorial_.