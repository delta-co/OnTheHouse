import flask; from flask import request, render_template
import recipedb

#from PIL import Image

from voussoirkit import pathclass
image_dir = pathclass.Path(__file__).parent.with_child('sample_images')

from .. import jsonify   

from . import common

site = common.site

@site.route('/recipe/<recipeid>/newreview')
@site.route('/recipe/<recipeid>/<slug>/newreview')
def create_review_page(recipeid, slug=None):
    recipe = common.rdb.get_recipe(recipeid)
    return flask.render_template('newreview.html', recipe=recipe, session_user=common.get_session(request))

@site.route('/recipe/<recipeid>/newreview', methods=['POST'])
@site.route('/recipe/<recipeid>/<slug>/newreview', methods=['POST'])
def post_review(recipeid, slug=None):
    recipe = common.rdb.get_recipe(recipeid)
    user = common.get_session(request)
    score = request.form['score']
    text = request.form['text']

    review = common.rdb.new_review(
        recipe = recipe,
        user = user,
        score = score,
        text = text,
    )

    response = jsonify.make_json_response({'reviewid': review.id})

    return response
