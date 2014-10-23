__author__ = 'Ralph'

import os
import os.path
from datetime import datetime
from elasticsearch import Elasticsearch


def create_index(index_name, definition):
    # es.indices.create(index="file-index", ignore=400)
    # run create_index.sh to create index
    pass


def drop_index(index_name):
    pass


def check_already_exists(fullname):
    # to do
    return True


def scan_and_push2es(root_folder):
    """
    parse files under root_folder and push to ES server
    root_folder should be a unicode string to support
    unicode file and folder names
    """
    assert root_folder[:2] == r'\\'

    machine = root_folder[2:][0:root_folder[2:].find('\\')]
    es = Elasticsearch()

    for root, dirs, files in os.walk(root_folder):
        for name in files:
            try:
                fullname = (os.path.join(root, name)).encode('utf-8')
                if check_already_exists(fullname):
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
                    es.index(index="file-index", doc_type='file', body=doc)
            except Exception, e:
                print e


if __name__ == '__main__':
    scan_and_push2es(ur'\\chn-yawen\shared')
    scan_and_push2es(ur'\\chn-xihou1\share')
    scan_and_push2es(ur'\\corp\china\Public Folders')