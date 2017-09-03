from flask import Blueprint

datatable = Blueprint('datatable', __name__)

from . import  views
