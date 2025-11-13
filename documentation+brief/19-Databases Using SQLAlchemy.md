# 19: Databases Using SQLAlchemy — The Pyramid Web Framework v2.0.2
Store and retrieve data using the SQLAlchemy ORM atop the SQLite database.

Background
-------------------------------------------------

Our Pyramid-based wiki application now needs database-backed storage of pages. This frequently means an SQL database. The Pyramid community strongly supports the [SQLAlchemy](https://docs.sqlalchemy.org/en/20/index.html#index-toplevel "(in SQLAlchemy v2.0)") project and its [object-relational mapper (ORM)](https://docs.sqlalchemy.org/en/20/orm/index.html#orm-toplevel "(in SQLAlchemy v2.0)") as a convenient, Pythonic way to interface to databases.

In this step we hook up SQLAlchemy to a SQLite database table, providing storage and retrieval for the wiki pages in the previous step.

Note

The Pyramid cookiecutter `pyramid-cookiecutter-starter` is really helpful for getting a SQLAlchemy project going, including generation of the console script. Since we want to see all the decisions, we will forgo convenience in this tutorial, and wire it up ourselves.

Objectives
-------------------------------------------------

*   Store pages in SQLite by using SQLAlchemy models.
    
*   Use SQLAlchemy queries to list/add/view/edit pages.
    
*   Provide a database-initialize command by writing a Pyramid _console script_ which can be run from the command line.
    

Steps
---------------------------------------

1.  We are going to use the forms step as our starting point:
    
    ```
cd ..; cp -r forms databases; cd databases

```

    
2.  We need to add some dependencies in `databases/setup.py` as well as an [entry point](about:blank/glossary.html#term-entry-point) for the command-line script:
    
    ```
 1from setuptools import setup
 2
 3# List of dependencies installed via `pip install -e .`
 4# by virtue of the Setuptools `install_requires` value below.
 5requires = [
 6    'deform',
 7    'pyramid',
 8    'pyramid_chameleon',
 9    'pyramid_tm',
10    'sqlalchemy',
11    'waitress',
12    'zope.sqlalchemy',
13]
14
15# List of dependencies installed via `pip install -e ".[dev]"`
16# by virtue of the Setuptools `extras_require` value in the Python
17# dictionary below.
18dev_requires = [
19    'pyramid_debugtoolbar',
20    'pytest',
21    'webtest',
22]
23
24setup(
25    name='tutorial',
26    install_requires=requires,
27    extras_require={
28        'dev': dev_requires,
29    },
30    entry_points={
31        'paste.app_factory': [
32            'main = tutorial:main'
33        ],
34        'console_scripts': [
35            'initialize_tutorial_db = tutorial.initialize_db:main'
36        ],
37    },
38)

```

    
    Note
    
    We aren't yet doing `$VENV/bin/pip install -e .` because we need to write a script and update configuration first.
    
3.  Our configuration file at `databases/development.ini` wires together some new pieces:
    
    ```
[app:main]
use = egg:tutorial
pyramid.reload_templates = true
pyramid.includes =
    pyramid_debugtoolbar
    pyramid_tm

sqlalchemy.url = sqlite:///%(here)s/sqltutorial.sqlite

[server:main]
use = egg:waitress#main
listen = localhost:6543

# Begin logging configuration

[loggers]
keys = root, tutorial, sqlalchemy.engine.Engine

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

[logger_sqlalchemy.engine.Engine]
level = INFO
handlers =
qualname = sqlalchemy.engine.Engine

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration

```

    
4.  This engine configuration now needs to be read into the application through changes in `databases/tutorial/__init__.py`:
    
    ```
 1from pyramid.config import Configurator
 2
 3from sqlalchemy import engine_from_config
 4
 5from .models import DBSession, Base
 6
 7def main(global_config, **settings):
 8    engine = engine_from_config(settings, 'sqlalchemy.')
 9    DBSession.configure(bind=engine)
10    Base.metadata.bind = engine
11
12    config = Configurator(settings=settings,
13                          root_factory='tutorial.models.Root')
14    config.include('pyramid_chameleon')
15    config.add_route('wiki_view', '/')
16    config.add_route('wikipage_add', '/add')
17    config.add_route('wikipage_view', '/{uid}')
18    config.add_route('wikipage_edit', '/{uid}/edit')
19    config.add_static_view('deform_static', 'deform:static/')
20    config.scan('.views')
21    return config.make_wsgi_app()

```

    
5.  Make a command-line script at `databases/tutorial/initialize_db.py` to initialize the database:
    
    ```
 1import os
 2import sys
 3import transaction
 4
 5from sqlalchemy import engine_from_config
 6
 7from pyramid.paster import (
 8    get_appsettings,
 9    setup_logging,
10    )
11
12from .models import (
13    DBSession,
14    Page,
15    Base,
16    )
17
18
19def usage(argv):
20    cmd = os.path.basename(argv[0])
21    print('usage: %s <config_uri>\n'
22          '(example: "%s development.ini")' % (cmd, cmd))
23    sys.exit(1)
24
25
26def main(argv=sys.argv):
27    if len(argv) != 2:
28        usage(argv)
29    config_uri = argv[1]
30    setup_logging(config_uri)
31    settings = get_appsettings(config_uri)
32    engine = engine_from_config(settings, 'sqlalchemy.')
33    DBSession.configure(bind=engine)
34    Base.metadata.create_all(engine)
35    with transaction.manager:
36        model = Page(title='Root', body='<p>Root</p>')
37        DBSession.add(model)

```

    
6.  Now that we've got all the pieces ready, and because we changed `setup.py`, we now install all the goodies:
    
    ```
$VENV/bin/pip install -e .

```

    
7.  The script references some models in `databases/tutorial/models.py`:
    
    ```
 1from pyramid.authorization import Allow, Everyone
 2
 3from sqlalchemy import (
 4    Column,
 5    Integer,
 6    Text,
 7    )
 8
 9from sqlalchemy.ext.declarative import declarative_base
10
11from sqlalchemy.orm import (
12    scoped_session,
13    sessionmaker,
14    )
15
16from zope.sqlalchemy import register
17
18DBSession = scoped_session(sessionmaker())
19register(DBSession)
20Base = declarative_base()
21
22
23class Page(Base):
24    __tablename__ = 'wikipages'
25    uid = Column(Integer, primary_key=True)
26    title = Column(Text, unique=True)
27    body = Column(Text)
28
29
30class Root:
31    __acl__ = [(Allow, Everyone, 'view'),
32               (Allow, 'group:editors', 'edit')]
33
34    def __init__(self, request):
35        pass

```

    
8.  Let's run this console script, thus producing our database and table:
    
    ```
$VENV/bin/initialize_tutorial_db development.ini

2016-04-16 13:01:33,055 INFO  [sqlalchemy.engine.Engine][MainThread] SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1
2016-04-16 13:01:33,055 INFO  [sqlalchemy.engine.Engine][MainThread] ()
2016-04-16 13:01:33,056 INFO  [sqlalchemy.engine.Engine][MainThread] SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1
2016-04-16 13:01:33,056 INFO  [sqlalchemy.engine.Engine][MainThread] ()
2016-04-16 13:01:33,057 INFO  [sqlalchemy.engine.Engine][MainThread] PRAGMA table_info("wikipages")
2016-04-16 13:01:33,057 INFO  [sqlalchemy.engine.Engine][MainThread] ()
2016-04-16 13:01:33,058 INFO  [sqlalchemy.engine.Engine][MainThread]
CREATE TABLE wikipages (
       uid INTEGER NOT NULL,
       title TEXT,
       body TEXT,
       PRIMARY KEY (uid),
       UNIQUE (title)
)


2016-04-16 13:01:33,058 INFO  [sqlalchemy.engine.Engine][MainThread] ()
2016-04-16 13:01:33,059 INFO  [sqlalchemy.engine.Engine][MainThread] COMMIT
2016-04-16 13:01:33,062 INFO  [sqlalchemy.engine.Engine][MainThread] BEGIN (implicit)
2016-04-16 13:01:33,062 INFO  [sqlalchemy.engine.Engine][MainThread] INSERT INTO wikipages (title, body) VALUES (?, ?)
2016-04-16 13:01:33,063 INFO  [sqlalchemy.engine.Engine][MainThread] ('Root', '<p>Root</p>')
2016-04-16 13:01:33,063 INFO  [sqlalchemy.engine.Engine][MainThread] COMMIT

```

    
9.  With our data now driven by SQLAlchemy queries, we need to update our `databases/tutorial/views.py`:
    
    ```
 1import colander
 2import deform.widget
 3
 4from pyramid.httpexceptions import HTTPFound
 5from pyramid.view import view_config
 6
 7from .models import DBSession, Page
 8
 9
10class WikiPage(colander.MappingSchema):
11    title = colander.SchemaNode(colander.String())
12    body = colander.SchemaNode(
13        colander.String(),
14        widget=deform.widget.RichTextWidget()
15    )
16
17
18class WikiViews:
19    def __init__(self, request):
20        self.request = request
21
22    @property
23    def wiki_form(self):
24        schema = WikiPage()
25        return deform.Form(schema, buttons=('submit',))
26
27    @property
28    def reqts(self):
29        return self.wiki_form.get_widget_resources()
30
31    @view_config(route_name='wiki_view', renderer='wiki_view.pt')
32    def wiki_view(self):
33        pages = DBSession.query(Page).order_by(Page.title)
34        return dict(title='Wiki View', pages=pages)
35
36    @view_config(route_name='wikipage_add',
37                 renderer='wikipage_addedit.pt')
38    def wikipage_add(self):
39        form = self.wiki_form.render()
40
41        if 'submit' in self.request.params:
42            controls = self.request.POST.items()
43            try:
44                appstruct = self.wiki_form.validate(controls)
45            except deform.ValidationFailure as e:
46                # Form is NOT valid
47                return dict(form=e.render())
48
49            # Add a new page to the database
50            new_title = appstruct['title']
51            new_body = appstruct['body']
52            DBSession.add(Page(title=new_title, body=new_body))
53
54            # Get the new ID and redirect
55            page = DBSession.query(Page).filter_by(title=new_title).one()
56            new_uid = page.uid
57
58            url = self.request.route_url('wikipage_view', uid=new_uid)
59            return HTTPFound(url)
60
61        return dict(form=form)
62
63
64    @view_config(route_name='wikipage_view', renderer='wikipage_view.pt')
65    def wikipage_view(self):
66        uid = int(self.request.matchdict['uid'])
67        page = DBSession.query(Page).filter_by(uid=uid).one()
68        return dict(page=page)
69
70
71    @view_config(route_name='wikipage_edit',
72                 renderer='wikipage_addedit.pt')
73    def wikipage_edit(self):
74        uid = int(self.request.matchdict['uid'])
75        page = DBSession.query(Page).filter_by(uid=uid).one()
76
77        wiki_form = self.wiki_form
78
79        if 'submit' in self.request.params:
80            controls = self.request.POST.items()
81            try:
82                appstruct = wiki_form.validate(controls)
83            except deform.ValidationFailure as e:
84                return dict(page=page, form=e.render())
85
86            # Change the content and redirect to the view
87            page.title = appstruct['title']
88            page.body = appstruct['body']
89            url = self.request.route_url('wikipage_view', uid=uid)
90            return HTTPFound(url)
91
92        form = self.wiki_form.render(dict(
93            uid=page.uid, title=page.title, body=page.body)
94        )
95
96        return dict(page=page, form=form)

```

    
10.  Our tests in `databases/tutorial/tests.py` changed to include SQLAlchemy bootstrapping:
     
     ```
 1import unittest
 2import transaction
 3
 4from pyramid import testing
 5
 6
 7def _initTestingDB():
 8    from sqlalchemy import create_engine
 9    from .models import (
10        DBSession,
11        Page,
12        Base
13        )
14    engine = create_engine('sqlite://')
15    Base.metadata.create_all(engine)
16    DBSession.configure(bind=engine)
17    with transaction.manager:
18        model = Page(title='FrontPage', body='This is the front page')
19        DBSession.add(model)
20    return DBSession
21
22
23class WikiViewTests(unittest.TestCase):
24    def setUp(self):
25        self.session = _initTestingDB()
26        self.config = testing.setUp()
27
28    def tearDown(self):
29        self.session.remove()
30        testing.tearDown()
31
32    def test_wiki_view(self):
33        from tutorial.views import WikiViews
34
35        request = testing.DummyRequest()
36        inst = WikiViews(request)
37        response = inst.wiki_view()
38        self.assertEqual(response['title'], 'Wiki View')
39
40
41class WikiFunctionalTests(unittest.TestCase):
42    def setUp(self):
43        from pyramid.paster import get_app
44        app = get_app('development.ini')
45        from webtest import TestApp
46        self.testapp = TestApp(app)
47
48    def tearDown(self):
49        from .models import DBSession
50        DBSession.remove()
51
52    def test_it(self):
53        res = self.testapp.get('/', status=200)
54        self.assertIn(b'Wiki: View', res.body)
55        res = self.testapp.get('/add', status=200)
56        self.assertIn(b'Add/Edit', res.body)

```

     
11.  Run the tests in your package using `pytest`:
     
     ```
$VENV/bin/pytest tutorial/tests.py -q
..
2 passed in 1.41 seconds

```

     
12.  Run your Pyramid application with:
     
     ```
$VENV/bin/pserve development.ini --reload

```

     
13.  Open [http://localhost:6543/](http://localhost:6543/) in a browser.
     

Analysis
---------------------------------------------

Let's start with the dependencies. We made the decision to use `SQLAlchemy` to talk to our database. We also, though, installed `pyramid_tm` and `zope.sqlalchemy`. Why?

Pyramid has a strong orientation towards support for `transactions`. Specifically, you can install a transaction manager into your application either as middleware or a Pyramid "tween". Then, just before you return the response, all transaction-aware parts of your application are executed.

This means Pyramid view code usually doesn't manage transactions. If your view code or a template generates an error, the transaction manager aborts the transaction. This is a very liberating way to write code.

The `pyramid_tm` package provides a "tween" that is configured in the `development.ini` configuration file. That installs it. We then need a package that makes SQLAlchemy, and thus the RDBMS transaction manager, integrate with the Pyramid transaction manager. That's what `zope.sqlalchemy` does.

Where do we point at the location on disk for the SQLite file? In the configuration file. This lets consumers of our package change the location in a safe (non-code) way. That is, in configuration. This configuration-oriented approach isn't required in Pyramid; you can still make such statements in your `__init__.py` or some companion module.

The `initialize_tutorial_db` is a nice example of framework support. You point your setup at the location of some `[console_scripts]`, and these get generated into your virtual environment's `bin` directory. Our console script follows the pattern of being fed a configuration file with all the bootstrapping. It then opens SQLAlchemy and creates the root of the wiki, which also makes the SQLite file. Note the `with transaction.manager` part that puts the work in the scope of a transaction, as we aren't inside a web request where this is done automatically.

The `models.py` does a little bit of extra work to hook up SQLAlchemy into the Pyramid transaction manager. It then declares the model for a `Page`.

Our views have changes primarily around replacing our dummy dictionary-of-dictionaries data with proper database support: list the rows, add a row, edit a row, and delete a row.