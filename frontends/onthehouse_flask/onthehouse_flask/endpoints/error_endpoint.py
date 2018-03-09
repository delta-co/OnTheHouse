from flask import render_template

from . import common

site = common.site


@site.errorhandler(404)
def error404(e):
    response = render_template("404.html"), 404
    return response


@site.errorhandler(500)
def error505(e):
    response = render_template("500.html"), 500
    return response
