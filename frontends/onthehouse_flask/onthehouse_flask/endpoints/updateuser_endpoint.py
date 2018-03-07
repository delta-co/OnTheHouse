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
    try:
        displayname = request.form['displayname']
        password = request.form['new password']
        password2 = request.form['re-enter password']
        blurb = request.form['blurb']
        uimage = request.files['user image']
    except:
        pass

    user = common.get_session(request)

    if password != "":
        if password != password2:
            flash('Passwords must match')
            flask.abort(403)
        user.set_password(password)

    if displayname != "":
        user.set_display_name(displayname)

    if blurb != "":
        user.set_bio_text(blurb)

    if uimage.filename != None:
        uimage.save = secure_filename(uimage.filename)
        userimage = common.rdb.new_image(uimage)
        user.set_profile_image(userimage)

    response = jsonify.make_json_response({'username': user.username})

    return response