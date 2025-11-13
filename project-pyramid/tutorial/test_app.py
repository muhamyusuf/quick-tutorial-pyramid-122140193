import pathlib
import tempfile
import unittest

import transaction
from pyramid import testing
from webtest import TestApp

from .models import DBSession, Page, get_base


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_counter(self):
        from .views import TutorialViews

        request = testing.DummyRequest()
        views = TutorialViews(request)
        data = views.home()
        self.assertEqual(data["name"], "Home View")
        self.assertEqual(data["counter"], 1)

    def test_plain_response(self):
        from .views import TutorialViews

        request = testing.DummyRequest(params={"name": "Alice"})
        views = TutorialViews(request)
        response = views.plain()
        self.assertIn(b"Alice", response.body)


class WikiFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        db_path = pathlib.Path(self.tempdir.name) / "test.sqlite"
        from tutorial import main

        settings = {
            "tutorial.secret": "test",
            "sqlalchemy.url": f"sqlite:///{db_path}",
        }
        app = main({}, **settings)
        base = get_base()
        base.metadata.create_all(DBSession.bind)
        self.engine = DBSession.bind
        with transaction.manager:
            DBSession.add(Page(uid="uid1", title="Test Page", body="<p>Body</p>"))
        self.testapp = TestApp(app)

    def tearDown(self):
        DBSession.remove()
        if getattr(self, "engine", None) is not None:
            self.engine.dispose()
        self.tempdir.cleanup()

    def test_wiki_listing(self):
        res = self.testapp.get("/wiki", status=200)
        self.assertIn(b"Test Page", res.body)

    def test_plain_endpoint(self):
        res = self.testapp.get("/plain?name=Tester", status=200)
        self.assertIn(b"Tester", res.body)
