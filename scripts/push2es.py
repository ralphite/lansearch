__author__ = 'yawen'

from elasticsearch import Elasticsearch

es = Elasticsearch()
es.indices.create(index="file-index", ignore=400)

i = 1
for line in open('files.csv'):
    if line.startswith('"'):
        line = line[1:]
        line = line[:len(line) - 1]
        ls = line.split('","')
        # machine,path,name,size,mtime,added,deleted
        full = "//" + ls[0] + ls[1] + "/" + ls[2]
        doc = {
            'machine': ls[0],
            'path': ls[1],
            'name': ls[2],
            'size': ls[3],
            'mtime': ls[4],
            'full': full
        }
        es.index(index="file-index", doc_type='file', id=i, body=doc)
        i += 1