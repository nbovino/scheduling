from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo, InputRequired)
from wtforms.fields.html5 import DateField


import app
import web_app

class Add_Store_Form(Form):
    store_name = SelectField("Name", validators=[DataRequired()], coerce=int) # First arg becomes the id element in the html
    store_number = StringField("Number", validators=[DataRequired()])
    street_number = StringField("Street Number", validators=[DataRequired()])
    street_name = StringField("Street Name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = IntegerField("Zip Code", validators=[DataRequired()])


class Add_Employee_Form(Form):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    address_num = StringField("Add Num", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = IntegerField("Zip", validators=[DataRequired()])
    phone = IntegerField("Phone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    work_level = SelectField("Job Required", choices=[(1, "Level 1"), (2, "Level 2"), (3, "Elite")], coerce=int)
    hire_date = DateField("Hire Date", validators=[InputRequired()], format="%m/%d/%Y")

    # def validate(self):
    #     res = super(Add_Employee_Form, self).validate()
    #     return res


class Add_Retailer_Form(Form):
    name = StringField("Retailer", validators=[DataRequired()])


class Add_Client_Form(Form):
    name = StringField("Client", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=100)])


class Add_Job_Form(Form):
    client = SelectField("Client", coerce=int)
    retailer = SelectField("Retailer", coerce=int)
    store = SelectField("Store", coerce=int)
    required_level = SelectField("Job Required", choices=[(1, "Level 1"), (2, "Level 2"), (3, "Elite")], coerce=int)
    start_date = DateField("Start Date", validators=[InputRequired()], format="%m/%d/%Y")
    end_date = DateField("End Date", validators=[InputRequired()], format="%m/%d/%Y")


    # def validate(self):
    #     res = super(Add_Job_Form, self).validate()
    #     return res
    # start_date = DateField()
    # end_date = DateField()

    # start_da = DateField("Hire Date", validators=[InputRequired()], format="%m/%d/%Y")
    #
    # def validate(self):
    #     res = super(Add_Job_Form, self).validate()
    #     return res
    # def validate(start_date):
    #     res = super(Date_Test_Form, start_date).validate()
    #     return res
    #
    # def validate_on_submit(self):

class Assign_Form(Form):
    assign = SelectField("Assigned", coerce=int)
    temp = SelectField("Temporary", coerce=int)

# Select fields with dynamic choice values:
#
# class UserDetails(Form):
#     group_id = SelectField(u'Group', coerce=int)
#
# def edit_user(request, id):
#     user = User.query.get(id)
#     form = UserDetails(request.POST, obj=user)
#     form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]

# class NonValidatingSelectField(SelectField):
#     def pre_validate(self, form):
#         pass
#
#
# class Add_Job_Form(Form):
#     retailer = SelectField(u'Retailer', choices=[app.get_all_retailers()], coerce=int)
#     store = NonValidatingSelectField(u'Model', choices=[])
#
#     def validate_retailer(self, field):
#         choices = app.get_stores_of_retailer(self.retailer.data)


class Date_Test_Form(Form):
    dt = DateField("Hire Date", validators=[InputRequired()], format="%m/%d/%Y")

    # def validate(self):
    #     res = super(Date_Test_Form, self).validate()
    #     return res