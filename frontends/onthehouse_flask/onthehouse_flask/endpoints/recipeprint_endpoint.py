from flask import request, render_template

import recipedb

from . import common

site = common.site


@site.route('/recipe/<recipeid>/print')
@site.route('/recipe/<recipeid>/<slug>/print')
def get_recipeprint(recipeid, slug=None):
    recipe = common.rdb.get_recipe(recipeid)
    response = render_template("recipeprint.html", recipe=recipe, session_user=common.get_session(request))
    return response