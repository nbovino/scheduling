
from flask import (Flask, g, render_template, flash, jsonify, redirect, url_for, abort, session, request, Markup)
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from wtforms.fields.html5 import DateField

import app
import web_app_parts

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


@web_app.route('/')
def base():
    data = app.get_all_store_info()
    return render_template('base.html', time=datetime.datetime.now(), data=data)


@web_app.route('/add_store', methods=("GET", "POST"))
def add_store():
    form = forms.Add_Store_Form()
    form.store_name.choices = [(0, 'Choose a Retailer')] + list(app.get_all_retailers())
    if form.validate_on_submit():
        if (app.add_store(form.store_name.data, form.store_number.data, form.street_number.data,
                      form.street_name.data, form.city.data, form.state.data, form.zip.data)):# form data
            app.set_dt_for_store(form.store_name.data, int(form.store_number.data))
            redirect(url_for('add_store', message="Store Added"))
        else:
            redirect(url_for('add_store', message="Store likely already exists"))
    return render_template('add_store.html', form=form, time=datetime.datetime.now(),
                           app=app, stores=app.get_all_store_info())


@web_app.route('/add_employee', methods=("GET", "POST"))
def add_employee():
    form = forms.Add_Employee_Form()
    if form.validate_on_submit():
        if (app.add_employee(form.first_name.data, form.last_name.data, form.address_num.data, form.street.data,
                             form.city.data, form.state.data, form.zip.data, form.phone.data, form.email.data,
                             form.work_level.data, form.hire_date.data)):
            app.set_closest_rep_data_emp(app.get_employee_id_with_email(form.email.data)[0])
            redirect(url_for('add_employee'))
        else:
            redirect(url_for('add_employee'))
    return render_template('add_employee.html', form=form, time=datetime.datetime.now(), app=app)


@web_app.route('/add_retailer', methods=("GET", "POST"))
def add_retailer():
    form = forms.Add_Retailer_Form()
    if form.validate_on_submit():
        if app.add_retailer(form.name.data):
            redirect(url_for('add_retailer'))
        else:
            redirect(url_for('add_retailer'))
    return render_template('add_retailer.html', form=form, time=datetime.datetime.now(), retailers=app.get_all_retailers())


@web_app.route('/add_client', methods=("GET", "POST"))
def add_client():
    form = forms.Add_Client_Form()
    if form.validate_on_submit():
        if app.add_client(form.name.data, form.description.data):
            return redirect(url_for('add_client'))
        else:
            return redirect(url_for('add_client'))

    return render_template('add_client.html', form=form, time=datetime.datetime.now(), app=app)


@web_app.route('/add_job', methods=("GET", "POST"))
def add_job():
    form = forms.Add_Job_Form()
    form.client.choices = [('0', 'Select Client')] + list(app.get_all_clients())
    form.retailer.choices = [('0', 'Select Retailer')] + list(app.get_all_retailers())
    form.store.choices = [('0', 'Select Store')] + list(app.get_all_stores())
    if form.validate_on_submit():
        app.add_job(form.client.data, form.store.data, form.required_level.data, form.start_date.data, form.end_date.data)
        redirect(url_for('add_job'))
    return render_template('add_job.html', form=form, time=datetime.datetime.now(), app=app)


@web_app.route('/view_info', methods=("GET", "POST"))
def view_info():
    return render_template('view_info.html', time=datetime.datetime.now())


@web_app.route('/set_closest_reps', methods=("GET", "POST"))
def set_closest_reps():
    app.assign_closest_reps()
    app.write_to_json('retailers')
    app.write_to_json('clients')
    app.write_to_json('stores')
    app.write_to_json('employees')
    app.write_to_json('jobs')
    return redirect(url_for('automation'))


@web_app.route('/job<job>', methods=("GET", "POST"))
def view_individual_job(job):
    if job != '0':
        sql = "SELECT required_level FROM jobs WHERE job_id=" + str(job)
        app.cur.execute(sql)
        level = app.cur.fetchone()[0]
        form = forms.Assign_Form(request.form)
        form.assign.choices = [(0, 'Assign Rep')] + list(app.get_all_employee_names(level=level))
        form.temp.choices = [(0, 'Temporary')] + list(app.get_all_employee_names(level=level))

        if form.validate_on_submit():
            if form.assign.data != '0':
                app.assign_rep_to_job(int(form.assign.data), int(job))
            if form.temp.data != '0':
                app.assign_temp_rep_to_job(int(form.temp.data), int(job))
            app.write_to_json('jobs')

        sql = "SELECT temp_employee, assigned_employee, closest_qual_t_emp, " \
              "closest_qual_d_emp, client_id, store_id FROM jobs WHERE job_id=" + str(job)
        app.cur.execute(sql)
        store = app.cur.fetchone()
        sql = "SELECT retailer FROM stores WHERE store_id=" + str(store[5])
        app.cur.execute(sql)
        retailer = app.cur.fetchone()
        sql = "SELECT name FROM retailers WHERE id=" + str(retailer[0])
        app.cur.execute(sql)
        retailer_name = app.cur.fetchone()
        address = app.get_store_address(store[5])
        client_name = app.get_client_name(store[4])
        if store[3]:
            closest_d_emp = app.get_employee_name(store[3])
        else:
            closest_d_emp = ('Not Yet assigned',)
        if store[2]:
            closest_t_emp = app.get_employee_name(store[2])
        else:
            closest_t_emp = ('Not Yet Assigned',)
        if store[1]:
            assigned_emp = app.get_employee_name(store[1])
        else:
            assigned_emp = ('Not Yet Assigned',)
        if store[0]:
            temp_emp = app.get_employee_name(store[0])
        else:
            temp_emp = ('Not Yet Assigned',)

        time_emps = app.get_closest_rep_data(int(store[5]), 't')
        dist_emps = app.get_closest_rep_data(int(store[5]), 'd')

        all_time_emps = []
        all_dist_emps = []
        for emp in time_emps:
            name = app.get_employee_name(emp[0])[0]
            time = emp[2]
            all_time_emps.append([name, time])

        for emp in dist_emps:
            name = app.get_employee_name(emp[0])[0]
            dist = emp[3]
            all_dist_emps.append([name, dist])

        return render_template('view_individual_job.html', form=form, time=datetime.datetime.now(), job=job,
                               address=address[0],
                               name=retailer_name[0],
                               client=client_name[0],
                               closest_d=closest_d_emp[0],
                               closest_t=closest_t_emp[0],
                               assigned=assigned_emp[0],
                               temp=temp_emp[0],
                               time_list=all_time_emps,
                               dist_list=all_dist_emps,
                               app=app)

    else:
        return render_template('view_info.html', time=datetime.datetime.now())


@web_app.route('/store<store>', methods=("GET", "POST"))
def view_individual_store(store):
    store_info = app.get_all_store_info(store)
    retailer_name = app.get_retailer_name(store_info[1])[0]
    store_number = store_info[2]
    address = store_info[3]
    jobs_at_store = app.get_all_jobs(store)
    time_emps = app.get_closest_rep_data(store, 't')
    dist_emps = app.get_closest_rep_data(store, 'd')
    all_time_emps = []
    all_dist_emps = []
    for emp in time_emps:
        name = app.get_employee_name(emp[0])[0]
        time = emp[2]
        all_time_emps.append([name, time])
    for emp in dist_emps:
        name = app.get_employee_name(emp[0])[0]
        dist = emp[3]
        all_dist_emps.append([name, dist])

    return render_template('view_individual_store.html', time=datetime.datetime.now(),
                           retailer=retailer_name,
                           store_number=store_number,
                           address=address,
                           all_jobs=jobs_at_store,
                           time_list=all_time_emps,
                           dist_list=all_dist_emps,
                           app=app)


@web_app.route('/compare_distances', methods=("GET", "POST"))
def compare_distances():
    return render_template('compare_distances.html', time=datetime.datetime.now())


@web_app.route('/all_jobs', methods=("GET", "POST"))
def all_jobs():
    return render_template('all_jobs.html', time=datetime.datetime.now())


@web_app.route('/automation', methods=("GET", "POST"))
def automation():
    return render_template('automation.html', time=datetime.datetime.now())


@web_app.route('/coming_soon')
def coming_soon():
    return render_template('coming_soon.html', time=datetime.datetime.now())


@web_app.route('/test', methods=("GET", "POST"))
def test():
    form = forms.Date_Test_Form(request.form)
    if form.validate_on_submit():
        time = datetime.datetime.now()
        render_template('test.html', form=form, time=time, value=value)
    return render_template('test.html', form=form, time=datetime.datetime.now())


@web_app.route('/parts')
def parts_base():
    return render_template('parts/base.html', time=datetime.datetime.now())


if __name__ == '__main__':
    web_app.run(debug=DEBUG, host=HOST, port=PORT)