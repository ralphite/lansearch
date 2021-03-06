import os
import re
import sys
from time import time
from multiprocessing import Pool as ThreadPool
from datetime import datetime

from flask_script import Manager, Shell

from app import create_app, db
from utils.crawler import get_current_domain, get_machines_in_domain, get_shared_folders_list
from utils.helpers import query_yes_no, synchronized
from utils.es_wrapper import drop_index as drop, create_index as create, scan_and_push_to_es
from config.config import config, Config
from app.models import Machine, SharedFolder, SharedFile


# import configured env vars
if os.path.exists('config/.env'):
    for l in open('config/.env'):
        var = l.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

config_type = os.getenv('LANSEARCH_CONFIG') or 'default'
app = create_app(config_type)
manager = Manager(app)


# start code coverage
COV = None
if os.environ.get('LANSEARCH_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='*')
    COV.start()


# #######################################
# commands
# #######################################


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def drop_index():
    """
    drop file index
    """
    if query_yes_no('This will erase all data in this index. Continue?', default='no'):
        drop(Config.INDEX_NAME)


@manager.command
def create_index():
    """
    create file index
    """
    create(Config.INDEX_NAME, Config.INDEX_BODY)


@manager.command
def recreate_tables():
    """
    dangerous
    """
    if query_yes_no('This will erase all data in the database. Continue?', default='no'):
        db.drop_all()
        db.create_all()


@manager.command
def retrieve_machine_list(domain=None):
    """
    retrieve machine list in the current domain. result will be saved to
    machines table in data/machines.db
    """
    start_time = time()
    if not domain:
        domain = get_current_domain()

    with db.session.no_autoflush:
        for m in get_machines_in_domain(domain):
            machine = Machine()
            machine.name = m
            machine.domain = domain
            '''
            # del if existing
            old = Machine.query.filter_by(name=m).first()

            if old:
                db.session.delete(old)
                db.session.commit()
            '''
            db.session.add(machine)
            sys.stdout.write('.')
        db.session.commit()
        print ' Runtime:', time() - start_time, 'seconds'


@manager.command
def filter_machines(pattern=None):
    machines = Machine.query.all()
    res = [m for m in machines if re.match(pattern, m.name)]
    return res


def worker(machine):
    with app.app_context():
        try:
            for folder in get_shared_folders_list(
                    os.getenv('user'), os.getenv('password'),
                    os.getenv('localhost_name'), machine.name.encode('ascii', 'ignore')):
                sf = SharedFolder()
                sf.name = unicode(folder)
                sf.machine = machine.name.encode('ascii', 'ignore')
                db.session.add(sf)
                sys.stdout.write('.')
        except Exception, e:
            pass
        db.session.commit()


@manager.command
def retrieve_shared_folder_list(machine_list=None, pattern=None):
    """
    retrieve list of shared folders and save to DB.
    """
    machine_list = machine_list or Machine.query.all()
    machines = [m for m in machine_list if re.match(pattern, m.name)]

    start_time = time()

    pool = ThreadPool(Config.DISCOVER_SHARED_FOLDERS_THREADS)
    pool.map(worker, machines)

    print ' Runtime: ', time() - start_time, 'seconds'


@manager.command
def filter_shared_folders(pattern=None):
    folders = SharedFolder.query.all()
    res = [f for f in folders if re.match(pattern, f.name)]
    return res


@manager.command
def crawl(shared_folder_list=None, pattern=None):
    """
    crawl list of shared files and push to ES.
    """
    # shared_folder_list = [ur'\\chn-yawen\shared']
    shared_folder_list = shared_folder_list or SharedFolder.query.all()
    pattern = pattern or ''
    for folder in shared_folder_list:
        print folder,
        try:
            start_time = time()
            scan_and_push_to_es(unicode(str(folder)))
            print 'Runtime: ', time() - start_time, 'seconds'
        except Exception, e:
            pass


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