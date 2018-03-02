import flask; from flask import request, render_template, flash

import recipedb

from .. import jsonify
from . import common

site = common.site


def follow_unfollow_core(targetname, action):
    user = common.get_session(request)
    if user is None:
        flask.abort(403)

    target = common.rdb.get_user(username=targetname)

    if action == 'follow':
        user.follow(target)
    else:
        user.unfollow(target)

    response = jsonify.make_json_response({})
    return response

@site.route('/user/<username>/follow', methods=['POST'])
def post_follow_user(username):
    return follow_unfollow_core(targetname=username, action='follow')

@site.route('/user/<username>/unfollow', methods=['POST'])
def post_unfollow_user(username):
    return follow_unfollow_core(targetname=username, action='unfollow')
