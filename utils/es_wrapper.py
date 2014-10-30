__author__ = 'Ralph'

import os
import os.path
from datetime import datetime
from elasticsearch import Elasticsearch


def create_index(index_name, definition):
    # es.indices.create(index="file-index", ignore=400)
    # use shell script for now
    pass


def drop_index(index_name):
    # use shell script for now
    pass


def check_if_already_exists(fullname):
    # to do
    return True


def scan_and_push_to_es(root_folder):
    """
    scan files under root_folder and push to ES server
    :param root_folder: folder to scan in unicode
    :return: None
    """
    assert root_folder[:2] == r'\\'

    machine = root_folder[2:][0:root_folder[2:].find('\\')]
    es = Elasticsearch()

    for root, dirs, files in os.walk(root_folder):
        for name in files:
            try:
                fullname = (os.path.join(root, name)).encode('utf-8')
                if check_if_already_exists(fullname):
                    path = os.path.dirname(fullname)
                    size = os.path.getsize(fullname.decode('utf-8'))  # buggy when long name
                    mtime = os.path.getmtime(fullname.decode('utf-8'))  # buggy when long name
                    doc = {
                        'machine': machine,
                        'path': path,
                        'full': fullname,
                        'name': name,
                        'size': size,
                        'mtime': str(datetime.fromtimestamp(int(mtime)))
                    }
                    print '>' * 10, fullname
                    es.index(index="file-index", doc_type='file', body=doc)
            except Exception, e:
                print e


if __name__ == '__main__':
    try:
        scan_and_push_to_es(ur'\\chn-yawen\shared')
    except Exception, e:
        print e
    #scan_and_push_to_es(ur'\\chn-xihou1\share')
    #scan_and_push_to_es(ur'\\corp\china\Public Folders')