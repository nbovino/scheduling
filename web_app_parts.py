from flask import (Flask, g, render_template, flash, jsonify, redirect, url_for, abort, session, request, Markup)
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from wtforms.fields.html5 import DateField

import app

import datetime
# import models
# import json
from dateutil.parser import parse

# DEBUG = True
# PORT = 8000
# HOST = '0.0.0.0'

parts_app = Flask(__name__)
# parts_app.secret_key = "lkh23k4;2rl;lkfjWAKDFJ!"


@parts_app.route('/parts')
def base():
    return render_template('parts/base.html', time=datetime.datetime.now())

# if __name__ == '__main__':
#     parts_app.run(debug=DEBUG, host=HOST, port=PORT)