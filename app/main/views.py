__author__ = 'Yadong'

from flask import Flask, render_template, request, Blueprint

from utils.helpers import to_human_readable, gen_pagination_list, Result

from . import main, es


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')