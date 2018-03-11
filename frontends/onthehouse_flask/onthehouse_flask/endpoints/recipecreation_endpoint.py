import flask; from flask import request, render_template
import json
import recipedb

#from PIL import Image

from voussoirkit import pathclass
image_dir = pathclass.Path(__file__).parent.with_child('sample_images')

from .. import jsonify

from . import common

site = common.site

@site.route('/newrecipe')
def create_recipe_page():
    return flask.render_template(
        'editrecipe.html',
        action="publishing",
        session_user=common.get_session(request),
    )

@site.route('/newrecipe', methods=['POST'])
def post_recipe():
    recipename = request.form['recipe name']
    blurb = request.form['recipe blurb']
    countryoforigin = request.form['country of origin']
    cuisine = request.form['cuisine']
    mealtype = request.form['meal type']
    preptime = request.form['prep time']
    servingsize = request.form['serving size']
    ingredients = json.loads(request.form.get('ingredients'))
    keep_ingredients = []
    for ingredient in ingredients:
        if len(ingredient) != 4:
            continue
        ingredient = [i.strip() for i in ingredient]
        if ingredient[2] == '':
            continue
        keep_ingredients.append(ingredient)
    ingredients = keep_ingredients
    instructions = request.form['instructions'].strip()
    image = request.files.get('recipe image', None)

    user = common.get_session(request)

    if user==None:
        flask.abort(403)     

    if image != None:
        recipeimage = common.process_uploaded_image(image)
    else:
        recipeimage = None

    recipe = common.rdb.new_recipe(
        author= user,
        blurb= blurb,
        country_of_origin= countryoforigin,
        cuisine= cuisine,
        ingredients= ingredients,
        instructions= instructions,
        meal_type= mealtype,
        name= recipename,
        prep_time= preptime,
        serving_size= servingsize,
        recipe_image= recipeimage,
    )

    #if image != None:
        #recipe.set_recipe_pic(image)
    #    pass


    response = jsonify.make_json_response({'recipeid': recipe.id})

    return response
