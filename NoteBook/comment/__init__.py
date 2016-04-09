# -*- coding: utf-8 -*
from .forms import CommentForm
from flask import Blueprint

comment = Blueprint('comment', __name__)

from . import views
