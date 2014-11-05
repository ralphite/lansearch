__author__ = 'Yadong'

from time import time
from flask import jsonify, request

from . import api
from utils.crawler import get_current_domain as gcd, get_machines_in_domain


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