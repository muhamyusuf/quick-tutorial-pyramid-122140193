import logging
import uuid

import colander
import deform
import deform.widget
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import forget, remember
from pyramid.view import (
    forbidden_view_config,
    view_config,
    view_defaults,
)

from .models import DBSession, Page
from .security import USERS, check_password

log = logging.getLogger(__name__)


class WikiPageSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget(),
    )


@view_defaults(renderer="templates/home.pt")
class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @property
    def counter(self):
        session = self.request.session
        session["counter"] = session.get("counter", 0) + 1
        return session["counter"]

    @view_config(route_name="home")
    def home(self):
        log.debug("Rendering home view")
        return {
            "name": "Home View",
            "counter": self.counter,
            "logged_in": self.logged_in,
        }

    @view_config(route_name="plain")
    def plain(self):
        name = self.request.params.get("name", "No Name Provided")
        body = f"URL {self.request.url} with name: {name}"
        return Response(body=body, content_type="text/plain")

    @view_config(route_name="hello", renderer="templates/hello.jinja2", permission="edit")
    def hello(self):
        first = self.request.matchdict.get("first")
        last = self.request.matchdict.get("last")
        log.debug("Hello view for %s %s", first, last)
        return {
            "title": "Hello View",
            "first": first,
            "last": last,
        }

    @view_config(route_name="hello_json", renderer="json")
    def hello_json(self):
        return {"name": "Hello View", "counter": self.counter}

    @view_config(route_name="login", renderer="templates/login.pt")
    @forbidden_view_config(renderer="templates/login.pt")
    def login(self):
        request = self.request
        login_url = request.route_url("login")
        referrer = request.url
        if referrer == login_url:
            referrer = "/"
        came_from = request.params.get("came_from", referrer)

        message = ""
        login_value = ""
        password_value = ""
        if "form.submitted" in request.params:
            login_value = request.params["login"]
            password_value = request.params["password"]
            hashed = USERS.get(login_value)
            if hashed and check_password(password_value, hashed):
                headers = remember(request, login_value)
                return HTTPFound(location=came_from, headers=headers)
            message = "Failed login"

        return {
            "name": "Login",
            "message": message,
            "url": login_url,
            "came_from": came_from,
            "login": login_value,
            "password": password_value,
        }

    @view_config(route_name="logout")
    def logout(self):
        request = self.request
        headers = forget(request)
        return HTTPFound(location=request.route_url("home"), headers=headers)


class WikiViews:
    def __init__(self, request):
        self.request = request
        self.form = deform.Form(WikiPageSchema(), buttons=("submit",))

    def _form_resources(self):
        resources = self.form.get_widget_resources()
        return {
            "css": resources["css"],
            "js": resources["js"],
        }

    def _next_uid(self):
        return uuid.uuid4().hex[:8]

    @view_config(route_name="wiki_view", renderer="templates/wiki_view.pt", permission="view")
    def wiki_view(self):
        pages = DBSession.query(Page).order_by(Page.title).all()
        return {
            "pages": pages,
            "resources": self._form_resources(),
        }

    @view_config(route_name="wikipage_view", renderer="templates/wiki_page.pt", permission="view")
    def wikipage_view(self):
        uid = self.request.matchdict["uid"]
        page = DBSession.query(Page).filter_by(uid=uid).first()
        if page is None:
            raise HTTPFound(location=self.request.route_url("wiki_view"))
        return {"page": page}

    @view_config(route_name="wikipage_add", renderer="templates/wiki_form.pt", permission="edit")
    def wikipage_add(self):
        form = self.form
        if "submit" in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure as exc:
                return {"form": exc.render(), "resources": self._form_resources()}

            uid = self._next_uid()
            page = Page(uid=uid, title=appstruct["title"], body=appstruct["body"])
            DBSession.add(page)
            return HTTPFound(location=self.request.route_url("wikipage_view", uid=uid))

        return {
            "form": form.render(),
            "resources": self._form_resources(),
        }

    @view_config(route_name="wikipage_edit", renderer="templates/wiki_form.pt", permission="edit")
    def wikipage_edit(self):
        uid = self.request.matchdict["uid"]
        page = DBSession.query(Page).filter_by(uid=uid).first()
        if page is None:
            raise HTTPFound(location=self.request.route_url("wiki_view"))

        form = self.form
        if "submit" in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure as exc:
                return {
                    "form": exc.render(),
                    "resources": self._form_resources(),
                }

            page.title = appstruct["title"]
            page.body = appstruct["body"]
            return HTTPFound(location=self.request.route_url("wikipage_view", uid=uid))

        return {
            "form": form.render({"title": page.title, "body": page.body}),
            "resources": self._form_resources(),
        }
