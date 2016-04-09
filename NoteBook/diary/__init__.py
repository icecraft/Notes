# -*- coding: utf-8 -*
from flask import Blueprint

diary = Blueprint('diary', __name__)

from . import views
