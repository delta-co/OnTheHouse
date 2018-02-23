import flask; from flask import request, render_template
import recipedb

from .. import jsonify   

from . import common

site = common.site

@site.route('/newrecipe')
def create_recipe_page():
    return flask.render_template('newrecipe.html', session_user=common.get_session(request))

@site.route('/newrecipe', methods=['POST'])
def post_recipe():
    try:
        recipename = request.form['recipe name']
        blurb = request.form['recipe blurb']
        countryoforigin = request.form['country of origin']
        cuisine = request.form['cuisine']
        mealtype = request.form['meal type']
        preptime = request.form['prep time']
        servingsize = request.form['serving size']
        ingredient = request.form['ingredient']
        instructions = request.form['instructions']
        #image = request.form['image']
    except KeyError:
        flask.abort(400)

    if instructions == "":
        flash('Instructions cannot be blank')
        flask.abort(403)

    if ingredient == "":
        flash('Must have at least 1 ingredient')
        flask.abort(403)

    recipe = common.rdb.new_recipe(
        author= common.rdb.get_user(),
        blurb= blurb,
        country_of_origin= countryoforigin,
        cuisine= cuisine,
        ingredients= ingredient,
        instructions= instructions,
        meal_type= mealtype,
        name= recipename,
        prep_time= preptime,
        serving_size= servingsize,
        recipe_image= None,
    )
    response = jsonify.make_json_response({'recipeid': recipe.recipe_id})

    return response