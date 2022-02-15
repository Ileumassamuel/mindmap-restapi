import os
import click
from flask_migrate import Migrate
from app import create_app, db

# Import models
from app.models.mindmap import MindMap
from app.models.leaf import Leaf

app = create_app(os.getenv("FLASK_ENV") or "development")
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """ Run unit tests """
    import unittest

    if test_names:
        """ Run specific unit tests.
        Example:
        $ flask test tests.testLeafApi.py ...
        """
        tests = unittest.TestLoader().loadTestsFromNames(test_names)

    else:
        tests = unittest.TestLoader().discover("tests", pattern="test*.py")

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0

    # Return 1 if tests failed, won't reach here if succeeded.
    return 1
