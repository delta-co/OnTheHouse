from flask import request, render_template

import recipedb

from . import common

site = common.site

@site.route('/editrecipe/<recipeid>')
def edit_recipe_page(recipeid):
    recipe = common.rdb.get_recipe(recipeid)
    ingredient_list = recipe.get_ingredients()
    ingredients = []
    for ingredient in ingredient_list:
        ingredient_attribute_list = []
    if (ingredient.quantity):
        ingredient_attribute_list.append(ingredient.quantity)

    if (ingredient.prefix):
        ingredient_attribute_list.append(ingredient.prefix)

    if (ingredient.ingredient.name):
        ingredient_attribute_list.append(ingredient.ingredient.name)

    if (ingredient.suffix):
        ingredient_attribute_list.append(ingredient.suffix)

    ingredients.append(ingredient_attribute_list)
    response = render_template("editrecipe.html", recipe=recipe, session_user=common.get_session(request), ingredients = ingredients)
    return response

@site.route('/editrecipe/<recipeid>', methods=['POST'])
def edit_recipe(recipeid):
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

    #if image is not None:
    #    recipe_image = common.process_uploaded_image(image)
    #else:
    #    recipe_image = None

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

    common.rdb.get_recipe(recipeid).edit(
        blurb= blurb,
        country= countryoforigin,
        cuisine= cuisine,
        ingredients= ingredient_list,
        instructions= instructions,
        meal_type= mealtype,
        name= recipename,
        prep_time= preptime,
        recipe_image= recipe_image,
        serving_size= servingsize,
    )

    #if image != None:
      #recipe.set_recipe_pic(image)
    #    pass

    response = jsonify.make_json_response({'recipeid': recipe.id})
    return response
