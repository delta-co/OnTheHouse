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
    session_user = common.get_session(request)
    recipe = common.rdb.get_recipe(recipeid)
    if session_user is None:
        return flask.redirect('/recipe/%s/%s' % (recipe.id, recipe.slug))
    existing_review = session_user.get_review_for_recipe(recipe)
    return flask.render_template('newreview.html',
        recipe=recipe,
        existing_review=existing_review,
        session_user=session_user,
    )

@site.route('/recipe/<recipeid>/newreview', methods=['POST'])
@site.route('/recipe/<recipeid>/<slug>/newreview', methods=['POST'])
def post_review(recipeid, slug=None):
    session_user = common.get_session(request)
    if session_user is None:
        flask.abort(403)

    recipe = common.rdb.get_recipe(recipeid)
    score = request.form.get('score', None)
    text = request.form.get('text', None)
    existing_review = session_user.get_review_for_recipe(recipe)
    if existing_review is None:
        review = common.rdb.new_review(
            recipe = recipe,
            user = session_user,
            score = score,
            text = text,
        )
    else:
        existing_review.edit(score=score, text=text)
        review = existing_review

    response = jsonify.make_json_response({'recipeid': recipe.id, 'reviewid': review.id})

    return response
