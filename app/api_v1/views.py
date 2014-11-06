__author__ = 'Yadong'

from time import time
from flask import jsonify, request

from . import api, es
from utils.crawler import get_current_domain as gcd, get_machines_in_domain
from config.config import Config


@api.route('/get-current-domain')
def get_current_domain():
    try:
        domain = gcd()
        return jsonify({
            'domain': domain,
            'error': ''
        })
    except Exception, e:
        return jsonify({
            'domain': '',
            'error': str(e)
        })


@api.route('/get-machine-list')
def get_machine_list():
    try:
        domain = 'CORP'
        machine_list = []
        for m in get_machines_in_domain(domain):
            print m
            machine_list.append({'name': m, 'discovered_time': time()})
        return jsonify({
            'machineList': machine_list,
            'error': ''
        })
    except Exception, e:
        return jsonify({
            'machineList': '',
            'error': str(e)
        })


@api.route('/search')
def search():
    query_text = request.args.get('q', '', type=str)
    offset = request.args.get('p', 1, type=int)
    query_type = request.args.get('t', 'match', type=str)
    items_per_page = Config.ITEMS_PER_PAGE
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

    return jsonify({
        'queryText': query_text,
        'queryType': query_type,
        'offset': offset,
        'itemsPerPage': items_per_page,
        'searchResult': resp,
        'error': ''
    })