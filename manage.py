import os

from flask_script import Manager, Command, Shell

from app import app
from scripts.utils.crawler import get_current_domain


manager = Manager(app)

COV = None  # code coverage
if os.environ.get('LANSEARCH_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='*')
    COV.start()


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test(enable_coverage=False):
    """
    Run unit tests
    :param enable_coverage:
    :return:
    """
    if enable_coverage and not os.environ.get("LANSEARCH_COVERAGE"):
        import sys

        os.environ["LANSEARCH_COVERAGE"] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestResult(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print('Code coverage:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname((__file__)))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML result: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def drop_index():
    """
    drop file index
    :return:
    """

    # to do


@manager.command
def create_index():
    """
    create file index
    :return:
    """

    # to do


@manager.command
def retrieve_machine_list(domain=None):
    """
    get
    :return:
    """

    if not domain:
        domain = get_current_domain()

        # to do


@manager.command
def retrieve_shared_folder_list(machine_list=None, machine_filter=None):
    """
    retrieve list of shared folders and save to ES.

    :param machine_filter:
    :return:
    """

    # to do


@manager.command
def crawl(shared_folder_list=None):
    """

    :param shared_folder_list:
    :return:
    """

    # to do


if __name__ == '__main__':
    manager.run()