from sqlalchemy import Column, Integer, Text, Unicode
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register as zope_register

DBSession = scoped_session(sessionmaker(expire_on_commit=False))
zope_register(DBSession)

Base = None


def get_base():
    global Base
    if Base is None:
        from sqlalchemy.orm import declarative_base

        Base = declarative_base()
    return Base


class Page(get_base()):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    uid = Column(Unicode(32), unique=True, nullable=False)
    title = Column(Unicode(200), nullable=False)
    body = Column(Text, nullable=False)


def includeme(config):
    settings = config.get_settings()
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    get_base().metadata.bind = engine
