from flask import Blueprint

echarts = Blueprint('echarts', __name__)

from . import  views
