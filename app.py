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
    test_results = [Result('link1', 'this is a file', 'hello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the details'
                                                      ' of the filehello this is the details of the f'
                                                      'ilehello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the d'
                                                      'etails of the filehello this is the details o'
                                                      'f the file'),
                    Result('link1', 'this is a file', 'hello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the details'
                                                      ' of the filehello this is the details of the f'
                                                      'ilehello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the d'
                                                      'etails of the filehello this is the details o'
                                                      'f the file'),
                    Result('link1', 'this is a file', 'hello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the details'
                                                      ' of the filehello this is the details of the f'
                                                      'ilehello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the d'
                                                      'etails of the filehello this is the details o'
                                                      'f the file'),
                    Result('link1', 'this is a file', 'hello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the details'
                                                      ' of the filehello this is the details of the f'
                                                      'ilehello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the d'
                                                      'etails of the filehello this is the details o'
                                                      'f the file'),
                    Result('link1', 'this is a file', 'hello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the details'
                                                      ' of the filehello this is the details of the f'
                                                      'ilehello this is the details of the filehello '
                                                      'this is the details of the filehello this is '
                                                      'the details of the filehello this is the d'
                                                      'etails of the filehello this is the details o'
                                                      'f the file'),
                    Result('link1', 'this is a file', 'hello this is the details of the file')]

    query_text = 'aaa'
    query_time = 0.032
    total_result_count = 132
    current_page = 2
    pages = [1, 2, 3, '..', 9]
    return render_template('search.html', results=test_results,
                           total_result_count=total_result_count,
                           query_text=query_text, query_time=query_time,
                           pages=pages, current_page=current_page)


if __name__ == '__main__':
    app.run(debug=True)