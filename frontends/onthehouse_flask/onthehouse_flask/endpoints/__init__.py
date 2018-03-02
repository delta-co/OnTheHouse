import flask; from flask import request
from flask_login import LoginManager
import random


from . import common
from . import image_endpoint
from . import ingredient_endpoint
from . import profile_endpoint
from . import recipe_endpoint
from . import register_endpoint
from . import recipecreation_endpoint
from . import updateuser_endpoint


site = common.site
loginmanager = LoginManager(site)


@site.route('/')
def root():
    all_recipes = common.rdb.get_recipes()
    session_user = common.get_session(request)

    user_recipes = []
    other_recipes = []
    if session_user:
        for recipe in all_recipes:
            if recipe.author == session_user:
                user_recipes.append(recipe)
            else:
                other_recipes.append(recipe)
    else:
        other_recipes = all_recipes

    return flask.render_template('home.html', user_recipes=user_recipes, other_recipes=other_recipes, session_user=session_user)

@site.route('/logout')
def user_logout():
    cookie_check = request.cookies.get(common.COOKIE_NAME, None)
    common.remove_cookie(cookie_check)
    return flask.redirect('/')


@site.route('/img/<imgid>')
def get_img(imgid):
    img = common.rdb.get_image(imgid)
    return flask.send_file(img.file_path)


@site.route('/favicon.ico')
@site.route('/favicon.png')
def favicon():
    return flask.send_file(common.FAVICON_PATH.absolute_path)


if __name__ == '__main__':
    #site.run(threaded=True)
    pass
