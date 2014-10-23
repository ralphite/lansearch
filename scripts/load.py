__author__ = 'Ralph'

import os
import os.path
from datetime import datetime
from elasticsearch import Elasticsearch


def load(root_folder):
    """
    parse files under root_folder and push to ES server
    root_folder should be a unicode string to support
    unicode file and folder names
    """

    es = Elasticsearch()
    # es.indices.create(index="file-index", ignore=400)
    # run create_index.sh to create index

    # root_folder = ur'\\corp\china\Public Folders'

    assert root_folder[:2] == r'\\'
    machine = root_folder[2:][0:root_folder[2:].find('\\')]

    for root, ds, files in os.walk(root_folder):
        for name in files:
            try:
                fullname = (os.path.join(root, name)).encode('utf-8')
                path = os.path.dirname(fullname)
                size = os.path.getsize(fullname.decode('utf-8'))
                mtime = os.path.getmtime(fullname.decode('utf-8'))
                doc = {
                    'machine': machine,
                    'path': path,
                    'full': fullname,
                    'name': name,
                    'size': size,
                    'mtime': str(datetime.fromtimestamp(int(mtime)))
                }
                es.index(index="file-index", doc_type='file', body=doc)
                #print doc
            except Exception, e:
                print e

if __name__ == '__main__':
    load(ur'\\chn-yawen\shared')
    load(ur'\\chn-xihou1\share')
    load(ur'\\corp\china\Public Folders')