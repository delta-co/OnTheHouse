import flask; from flask import request, render_template

from . import common

site = common.site


@site.route('/user/<username>')
def get_user(username):
    user = common.rdb.get_user(username = username)
    recipes = common.rdb.search(author=user)
    response = render_template("profile.html", user=user, recipes=recipes, session_user=common.get_session(request))
    return response


@site.route('/user/<username>/profilepic')
@site.route('/user/<username>/profilepic.<ext>')
def get_profile_pic(username, ext=None):
    user = common.rdb.get_user(username=username)
    if user.profile_image_id:
        image = common.rdb.get_image(id=user.profile_image_id)
        return flask.send_file(image.file_path)
    else:
        path = common.STATIC_DIR.with_child('default_profile_pic.jpg').absolute_path
        return flask.send_file(path)

@site.route('/user')
def user():
    response = render_template("profile-test.html", session_user=common.get_session(request))
    return response

@site.route('/feed')
def get_feed():
    user = common.get_session(request)
    if user is None:
        return flask.redirect('/login')

    response = render_template('feed.html', session_user=user)
    return response
