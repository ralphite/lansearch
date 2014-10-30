import os

from flask_script import Manager, Shell

from app.app import app
from utils.console import print_dot
from utils.crawler import get_current_domain, get_machines_in_domain, get_shared_folders_list


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
    retrieve machine list in the current domain. result will be saved to
    machines table in data/machines.db
    """

    if not domain:
        domain = get_current_domain()

    machines = get_machines_in_domain(domain)
    for i in range(10):
        print_dot()
        # need to use multi threading


@manager.command
def retrieve_shared_folder_list(machine_list=None, filter=None):
    """
    retrieve list of shared folders and save to ES.

    :param filter:
    :return:
    """

    # to do


@manager.command
@manager.option('-s', '--shared-folder-list', dest='shared_folder_list', default=None)
def crawl(shared_folder_list=None):
    """

    :param shared_folder_list:
    :return:
    """

    # to do


@manager.command
def test(enable_coverage=False):
    """
    Run unit tests
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
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML result: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()