from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo, InputRequired)
from wtforms.fields.html5 import DateField

class New_Part_Form(Form):
    store_name = SelectField("Name", validators=[DataRequired()], coerce=int) # First arg becomes the id element in the html
    store_number = StringField("Number", validators=[DataRequired()])
    street_number = StringField("Street Number", validators=[DataRequired()])
    street_name = StringField("Street Name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = IntegerField("Zip Code", validators=[DataRequired()])
