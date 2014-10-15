__author__ = 'Ralph'

from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()


class Result:
    def __init__(self, link, machine, path, name, size, mtime):
        self.link = link
        self.name = name
        self.machine = machine
        self.path = path
        self.size = size
        self.mtime = mtime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query_text = request.args.get('q', '', type=str)
    offset = request.args.get('p', 1, type=int)
    res = es.search(index="file-index", doc_type='file',
                    body={
                        "size": 100,
                        "from": (offset - 1 or 0) * 10,
                        "query": {
                            "match": {
                                "_all": query_text
                            }
                        }
                    })
    results = []
    for hit in res['hits']['hits']:
        r = Result(
            '\\\\' + hit['_source']['machine'] + '/shared/' + hit['_source']['path'] + '/' + hit['_source']['name'],
            hit['_source']['machine'], hit['_source']['path'],
            hit['_source']['name'], hit['_source']['size'],
            hit['_source']['mtime'])
        results.append(r)

    query_time = 0.032
    total_result_count = len(results)
    current_page = offset
    pages = [1, 2, 3, '..', 9]
    return render_template('search.html', results=results,
                           total_result_count=total_result_count,
                           query_text=query_text, query_time=query_time,
                           pages=pages, current_page=current_page)


if __name__ == '__main__':
    app.run(debug=True)