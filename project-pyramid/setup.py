from setuptools import setup, find_packages

requires = [
    "bcrypt",
    "deform",
    "pyramid",
    "pyramid_chameleon",
    "pyramid_debugtoolbar",
    "pyramid_jinja2",
    "pyramid_tm",
    "SQLAlchemy",
    "waitress",
    "zope.sqlalchemy",
]

tests_require = [
    "pytest",
    "webtest",
]

setup(
    name="tutorial",
    version="0.1.0",
    description="Pyramid quick tutorial bundle project",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    extras_require={
        "dev": [
            *tests_require,
        ],
    },
    entry_points={
        "paste.app_factory": [
            "main = tutorial:main",
        ],
        "console_scripts": [
            "initialize_tutorial_db = tutorial.initialize_db:main",
        ],
    },
)
