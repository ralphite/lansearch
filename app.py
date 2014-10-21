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


def to_human_readable(n):
    n = int(n)
    if n < 1024:
        return ('%.2f' % n) + ' Bytes'
    n /= 1024.0
    if n < 1024:
        return ('%.2f' % n) + ' KB'
    n /= 1024.0
    if n < 1024:
        return ('%.2f' % n) + ' MB'
    n /= 1024.0
    return ('%.2f' % n) + ' GB'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    query_text = request.args.get('q', '', type=str)
    # print query_text
    offset = request.args.get('p', 1, type=int)
    search_type = request.args.get('t', 'match', type=str)
    items_per_page = 20
    res = es.search(index="file-index", doc_type='file',
                    body={
                        "size": items_per_page,
                        "from": (offset - 1) * items_per_page,
                        "query": {
                            search_type: {
                                "full": query_text
                            }
                        }
                    })
    results = []
    for hit in res['hits']['hits']:
        machine = hit['_source']['machine']
        path = hit['_source']['path']
        name = hit['_source']['name']
        size = to_human_readable(hit['_source']['size'])
        mtime = hit['_source']['mtime']
        link = '//' + machine + path + '/' + name
        link = link.replace('/', '\\')
        if len(path) > 40:
            path = path[:37] + '...'
        if len(name) > 30:
            name = name[:27] + '...'
        r = Result(link, machine, path, name, size, mtime)
        results.append(r)

    query_time = str(res['took'] / 1000.0)
    total_result_count = res['hits']['total']
    current_page = offset
    page_count = total_result_count // items_per_page + 1
    pages = []
    if page_count > 10:
        if current_page < 7:
            pages = [i + 1 for i in range(7)]
            pages += ['..', page_count - 1, page_count]
        elif current_page > page_count - 7:
            pages = [1, 2, '..']
            pages += [page_count - 6 + i for i in range(7)]
        else:
            pages += [1, 2, 3, '..']
            pages += [current_page - 1, current_page, current_page + 1, '..']
            pages += [page_count - 1, page_count]
    else:
        pages = [i + 1 for i in range(page_count)]
    return render_template('search.html', results=results,
                           total_result_count=total_result_count,
                           query_text=query_text, query_time=query_time,
                           pages=pages, current_page=current_page,
                           query_type=search_type)


if __name__ == '__main__':
    app.run(debug=True)