#!/usr/bin/python3

"""create app_views which is an instance of Blueprint
(url prefix must be /api/v1)"""


from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
