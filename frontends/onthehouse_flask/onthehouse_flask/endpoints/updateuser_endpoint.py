import flask; from flask import request, render_template, flash

import recipedb; from recipedb import objects

from .. import jsonify
from . import common

site = common.site


@site.route('/updateuser')
def update_page():
    return flask.render_template('updateuser.html', session_user=common.get_session(request))

@site.route('/updateuser', methods=['POST'])
def post_update():
    display_name = request.form.get('displayname', None)
    password = request.form.get('new password', None)
    password2 = request.form.get('re-enter password', None)
    bio_text = request.form.get('bio text', None)
    uimage = request.files.get('user image', None)

    user = common.get_session(request)
    if user is None:
        flask.abort(403)

    if password == '':
        password = None

    if password is not None:
        if password != password2:
            #flash('Passwords must match')
            flask.abort(403)

    profile_image = common.process_uploaded_image(uimage)
    user.edit(
        bio_text=bio_text,
        display_name=display_name,
        password=password,
        profile_image=profile_image,
    )

    response = jsonify.make_json_response({'username': user.username})

    return response
