import flask; from flask import request
from flask_login import LoginManager
import random


from . import common
from . import image_endpoint
from . import profile_endpoint
from . import recipe_endpoint
from . import register_endpoint


site = common.site
loginmanager = LoginManager(site)


@site.route('/')
def root():
    recipes = common.rdb.get_recipes()
    return flask.render_template('home.html', recipes=recipes, session_user=common.get_session(request))


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
