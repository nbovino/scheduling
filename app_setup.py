from flask import (Flask, g, render_template, flash, jsonify, redirect, url_for, abort, session, request, Markup)
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from wtforms.fields.html5 import DateField

import app

import datetime
import forms
# import models
# import json
from dateutil.parser import parse

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

web_app = Flask(__name__)
web_app.secret_key = 'nfj2984ijNDUUu2j3kj32nlr3f)k23rj90wjdinoaIUFHEpyio'