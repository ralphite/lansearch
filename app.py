__author__ = 'Ralph'

from flask import Flask, render_template

app = Flask(__name__)


class Result:
    def __init__(self, link, name, details):
        self.link = link
        self.name = name
        self.details = details


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    results = [Result('link1', 'this is a file', '''
        this is the detailed info of the search result.this is the detailed info of the search result.
        this is the detailed info of the search result.this is the detailed info of the search result.
        this is the detailed info of the search result.this is the detailed info of the search result.
        this is the detailed info of the search result.this is the detailed info of the search result.
    ''')]
    results *= 6

    query_text = 'bbb'
    query_time = 0.032
    total_result_count = 132
    current_page = 2
    pages = [1, 2, 3, '..', 9]
    return render_template('search.html', results=results,
                           total_result_count=total_result_count,
                           query_text=query_text, query_time=query_time,
                           pages=pages, current_page=current_page)


if __name__ == '__main__':
    app.run(debug=True)