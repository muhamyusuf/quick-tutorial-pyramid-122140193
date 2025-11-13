import argparse

import transaction
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config

from .models import DBSession, Page, get_base


def main(argv=None):
    parser = argparse.ArgumentParser(description="Initialize the tutorial database.")
    parser.add_argument("config_uri", help="Path to PasteDeploy config file (development.ini)")
    args = parser.parse_args(argv)

    config_uri = args.config_uri
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    base = get_base()
    base.metadata.bind = engine
    base.metadata.create_all(engine)

    with transaction.manager:
        if not DBSession.query(Page).filter_by(uid="100").first():
            DBSession.add(
                Page(
                    uid="100",
                    title="Page 100",
                    body="<p>Sample page 100</p>",
                )
            )
        if not DBSession.query(Page).filter_by(uid="101").first():
            DBSession.add(
                Page(
                    uid="101",
                    title="Page 101",
                    body="<p>Sample page 101</p>",
                )
            )


if __name__ == "__main__":
    main()
