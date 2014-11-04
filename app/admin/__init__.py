__author__ = 'Yadong'

from flask import Blueprint
from elasticsearch import Elasticsearch

admin = Blueprint('admin', __name__)
es = Elasticsearch()

from . import views  # avoid circular import error