__author__ = 'Ralph'

from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

from utils.helpers import to_human_readable, gen_pagination_list, Result

from .import create_app

app = create_app()
es = Elasticsearch()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    query_text = request.args.get('q', '', type=str)
    offset = request.args.get('p', 1, type=int)
    query_type = request.args.get('t', 'match', type=str)
    items_per_page = 20
    resp = es.search(index="file-index", doc_type='file',
                     body={
                         "size": items_per_page,
                         "from": (offset - 1) * items_per_page,
                         "query": {
                             query_type: {
                                 "full": query_text
                             }
                         }
                     })
    results = []
    for hit in resp['hits']['hits']:
        machine = hit['_source']['machine']
        path = hit['_source']['path']
        name = hit['_source']['name']
        size = to_human_readable(hit['_source']['size'])
        mtime = hit['_source']['mtime']
        link = path + '/' + name
        link = link.replace('/', '\\')
        if len(path) > 40:
            path = path[:37] + '...'
        if len(name) > 30:
            name = name[:27] + '...'
        results.append(Result(link, machine, path, name, size, mtime))

    query_time = str(resp['took'] / 1000.0)
    total_result_count = resp['hits']['total']
    pages = gen_pagination_list(total_result_count // items_per_page + 1, offset)

    return render_template('search.html', results=results,
                           total_result_count=total_result_count,
                           query_text=query_text, query_time=query_time,
                           pages=pages, current_page=offset,
                           query_type=query_type)


if __name__ == '__main__':
    app.run(debug=True)