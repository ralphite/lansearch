__author__ = 'Yadong'

from flask import Blueprint
from elasticsearch import Elasticsearch

admin = Blueprint('admin', __name__)
es = Elasticsearch()

from . import views  # has to be at the end (after main
# declaration so that there is no nested import error