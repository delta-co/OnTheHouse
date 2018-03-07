import flask; from flask import request, render_template
import recipedb

#from PIL import Image

from voussoirkit import pathclass
image_dir = pathclass.Path(__file__).parent.with_child('sample_images')

from .. import jsonify   

from . import common

site = common.site

@site.route('/newrecipe')
def create_recipe_page():
    return flask.render_template('newrecipe.html', session_user=common.get_session(request))

@site.route('/newrecipe', methods=['POST'])
def post_recipe():
    recipename = request.form['recipe name']
    blurb = request.form['recipe blurb']
    countryoforigin = request.form['country of origin']
    cuisine = request.form['cuisine']
    mealtype = request.form['meal type']
    preptime = request.form['prep time']
    servingsize = request.form['serving size']
    ingredients = request.form.getlist('ingredients[]')
    ingredients = [i.strip() for i in ingredients]
    ingredients = [i for i in ingredients if i]
    instructions = request.form['instructions'].strip()
    #image = request.form['recipe image']

    user = common.get_session(request)

    '''
    if image != None:
        f = open('img', 'w+')
        f.write(image)
        rimage = common.rdb.new_image('img')
    else:
        rimage = None
    '''

    if user==None:
        flask.abort(403)     

    #if instructions == "":
    #   flash('Instructions cannot be blank')
    #    flask.abort(403)

    #if ingredients == "":
    #   flash('Must have at least 1 ingredient')
    #   flask.abort(403)

    ingredient_list = []
    for ingredient in ingredients:
        templist = ingredient.split(',')
        ingredient_list.append(templist)

    recipe = common.rdb.new_recipe(
        author= user,
        blurb= blurb,
        country_of_origin= countryoforigin,
        cuisine= cuisine,
        ingredients= ingredient_list,
        instructions= instructions,
        meal_type= mealtype,
        name= recipename,
        prep_time= preptime,
        serving_size= servingsize,
        recipe_image= None,
    )

    #if image != None:
        #recipe.set_recipe_pic(image)
    #    pass


    response = jsonify.make_json_response({'recipeid': recipe.id})

    return response
