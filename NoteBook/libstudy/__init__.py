# -*- coding: utf-8 -*
from flask import Blueprint

libstudy = Blueprint('libstudy', __name__)

from . import views
