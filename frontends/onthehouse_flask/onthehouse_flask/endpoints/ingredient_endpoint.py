from flask import request, render_template

import recipedb

from . import common

site = common.site

@site.route('/ingredient/<ingredientname>')
def get_ingredient(ingredientname):
    ingredient = common.rdb.get_ingredient_by_name(ingredientname)
    recipes = common.rdb.search(ingredients=[ingredient])
    response = render_template(
        "ingredient.html",
        ingredient=ingredient,
        recipes=recipes,
        session_user=common.get_session(request),
    )
    return response
