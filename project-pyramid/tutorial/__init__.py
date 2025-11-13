from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from .security import SecurityPolicy


def main(global_config, **settings):
    session_factory = SignedCookieSessionFactory("itsaseekreet")
    config = Configurator(
        settings=settings,
        session_factory=session_factory,
        root_factory="tutorial.resources.Root",
    )
    config.include("pyramid_chameleon")
    config.include("pyramid_jinja2")
    config.include(".models")

    secret = settings.get("tutorial.secret", "tutorial-secret")
    config.set_security_policy(SecurityPolicy(secret=secret))

    config.add_static_view(name="static", path="tutorial:static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("hello", "/howdy/{first}/{last}")
    config.add_route("plain", "/plain")
    config.add_route("hello_json", "/howdy.json")
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    config.add_route("wiki_view", "/wiki")
    config.add_route("wikipage_add", "/wiki/add")
    config.add_route("wikipage_view", "/wiki/{uid}")
    config.add_route("wikipage_edit", "/wiki/{uid}/edit")

    config.scan()
    return config.make_wsgi_app()
