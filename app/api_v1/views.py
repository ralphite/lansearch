__author__ = 'Yadong'

from flask import jsonify

from .import api
from utils.crawler import get_current_domain as gcd

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