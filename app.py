#!/usr/bin/env python
from __future__ import print_function

import calculate_distance
import db_connect
import json
import pymysql
import re
from datetime import *
from dateutil.parser import parse


conn = db_connect.connect_to_db()
cur = conn.cursor()


def get_all_employee_addresses():
    sql = "SELECT employee_id, CONCAT(first_name, ' ', last_name) as full_name, " \
        "CONCAT(address_num, ' ', street, '. ', " \
        "city, ', ', state, ' ' , zip) as full_address, work_level FROM employees ORDER BY last_name"
    cur.execute(sql)
    return cur.fetchall()


def get_employee_address(emp):
    sql = "SELECT CONCAT(address_num, ' ', street, '. ', city, ', ', state, ' ', zip) FROM employees " \
          "WHERE employee_id=" + str(emp)
    cur.execute(sql)
    return cur.fetchone()


def get_employee_name(emp):
    sql = "SELECT CONCAT(first_name, ' ', last_name) FROM employees WHERE employee_id=" + str(emp)
    cur.execute(sql)
    return cur.fetchone()


def get_employee_id_with_email(email):
    sql = "SELECT employee_id FROM employees WHERE email='" + email + "'"
    cur.execute(sql)
    return cur.fetchone()


def get_all_employee_names(level=None):
    sql = "SELECT employee_id, CONCAT(first_name, ' ', last_name) AS full_name FROM employees"
    if level:
        sql += " WHERE work_level >=" + str(level)
    cur.execute(sql)
    return cur.fetchall()


def get_all_store_info(store=None):
    sql = "SELECT store_id, retailer, number, " \
           "CONCAT(address_num, ' ', street, '. ', city, ', ', state, ' ' , zip) as full_address FROM stores"
    if store:
        sql += " WHERE store_id=" + str(store)
        cur.execute(sql)
        return cur.fetchone()
    sql += " ORDER BY retailer, number"
    cur.execute(sql)
    return cur.fetchall()


def get_store_address(store):
    sql = "SELECT CONCAT(address_num, ' ', street, '. ', city, ', ', state, ' ', zip) FROM stores " \
          "WHERE store_id=" + str(store)
    cur.execute(sql)
    return cur.fetchone()


def get_all_retailers():
    sql = "SELECT id, name FROM retailers"
    cur.execute(sql)
    return cur.fetchall()


def get_retailer_name(num):
    sql = "SELECT name FROM retailers WHERE id=" + str(num)
    cur.execute(sql)
    return cur.fetchone()


def get_retailer_id(name):
    sql = "SELECT id FROM retailers WHERE name='" + name + "'"
    cur.execute(sql)
    return cur.fetchone()


def get_all_clients():
    sql = "SELECT client_id, name FROM clients"
    cur.execute(sql)
    return cur.fetchall()


def get_client_name(client_id):
    sql = "SELECT name FROM clients WHERE client_id=" + str(client_id)
    cur.execute(sql)
    return cur.fetchone()


def get_all_jobs(store=None):
    sql = "SELECT job_id, client_id, store_id, required_level"
    if store:
        sql += ", assigned_employee FROM jobs WHERE store_id = " + str(store)
        cur.execute(sql)
        return cur.fetchall()
    sql += " FROM jobs ORDER BY client_id, store_id"
    cur.execute(sql)
    return cur.fetchall()


def get_all_stores():
    sql = "SELECT store_id, CONCAT(address_num, ' ', street, '. ', city, ', ', state, ' ' , zip) as full_address " \
          "FROM stores ORDER BY store_id, city"
    cur.execute(sql)
    return cur.fetchall()


def get_stores_of_retailer(retailer):
    sql = "SELECT store_id, CONCAT(number, ': ', address_num, ' ', street, '. ', city, ', ', state, ' ' , zip) " \
          "as store_info" \
          " FROM stores WHERE retailer=" + str(retailer)
    cur.execute(sql)
    return cur.fetchall()


def verify_new_data(store, emp):
    new_data = True
    sql = "SELECT dist_val FROM distance_time WHERE store_id=" + str(store) + " AND emp_id=" + str(emp)
    cur.execute(sql)
    results = cur.fetchone()
    if results:
        new_data = False
    return new_data


def create_closest_rep_data():
    # stores = get_all_stores()
    # employees = get_all_employee_names()
    for store in get_all_stores():
        store_add = store[1]
        for employee in get_all_employee_addresses():
            if verify_new_data(store[0], employee[0]):
                emp_add = employee[2]
                data = calculate_distance.get_distance(emp_add, store_add)
                time_val = data["rows"][0]["elements"][0]["duration"]["value"]
                dist_val = data["rows"][0]["elements"][0]["distance"]["value"]
                time_text = data["rows"][0]["elements"][0]["duration"]["text"]
                dist_text = data["rows"][0]["elements"][0]["distance"]["text"]
                sql = "INSERT INTO distance_time (store_id, emp_id, time_val, dist_val, time_text, dist_text) VALUES(" \
                      "" + str(store[0]) + ", " + str(employee[0]) + ", " + str(time_val) + ", " + str(dist_val) + ", "\
                    "\"" + time_text + "\", \"" + dist_text + "\")"
                cur.execute(sql)
                conn.commit()


# Writes to distance_time table when new store added
def set_closest_rep_data_store(store):
    store_add = get_store_address(store)
    for employee in get_all_employee_addresses():
        emp_add = employee[2]
        sql = "SELECT dist_val FROM distance_time WHERE store_id=" + str(store) + " AND emp_id=" + str(employee[0])
        results = cur.execute(sql)
        if not results:
            data = calculate_distance.get_distance(emp_add, store_add[0])
            time_val = data["rows"][0]["elements"][0]["duration"]["value"]
            dist_val = data["rows"][0]["elements"][0]["distance"]["value"]
            time_text = data["rows"][0]["elements"][0]["duration"]["text"]
            dist_text = data["rows"][0]["elements"][0]["distance"]["text"]
            sql = "INSERT INTO distance_time (store_id, emp_id, time_val, dist_val, time_text, dist_text) VALUES(" \
                  "" + str(store) + ", " + str(employee[0]) + ", " + str(time_val) + ", " + str(dist_val) + ", " \
                  "\"" + time_text + "\", \"" + dist_text + "\")"
            cur.execute(sql)
            conn.commit()
    write_to_json('stores')


# Writes to distance_time table when new employee added
def set_closest_rep_data_emp(emp):
    emp_add = get_employee_address(emp)
    for store in get_all_store_info():
        sql = "SELECT dist_val FROM distance_time WHERE store_id=" + str(store[0]) + " AND emp_id=" + str(emp)
        results = cur.execute(sql)
        if not results:
            data = calculate_distance.get_distance(emp_add[0], store[3])
            time_val = data["rows"][0]["elements"][0]["duration"]["value"]
            dist_val = data["rows"][0]["elements"][0]["distance"]["value"]
            time_text = data["rows"][0]["elements"][0]["duration"]["text"]
            dist_text = data["rows"][0]["elements"][0]["distance"]["text"]
            sql = "INSERT INTO distance_time (store_id, emp_id, time_val, dist_val, time_text, dist_text) VALUES(" \
                  "" + str(store[0]) + ", " + str(emp) + ", " + str(time_val) + ", " + str(dist_val) + ", " \
                  "\"" + time_text + "\", \"" + dist_text + "\")"
            cur.execute(sql)
            conn.commit()
    write_to_json('employees')


def get_closest_rep_data(store, d_t):
    sql = "SELECT emp_id, store_id, time_text, dist_text FROM distance_time WHERE store_id=" + str(store)
    if d_t == 't':
        sql += " ORDER BY time_val LIMIT 10"
    if d_t == 'd':
        sql += " ORDER BY dist_val LIMIT 10"
    cur.execute(sql)
    return cur.fetchall()


# Filled with non DRY code TODO: clean up at some point
def assign_closest_reps_to_store(store):
        closest_employee_dist = None
        closest_employee_time = None
        old_distance = 999999999999999
        old_time = 9999999999999999

        for emp in get_all_employee_addresses():
            emp_address = emp[2]
            store_address = get_store_address(store)
            data = calculate_distance.get_distance(emp_address, store_address[0])
            distance = data["rows"][0]["elements"][0]["distance"]["value"]
            time = data["rows"][0]["elements"][0]['duration']["value"]
            if distance < old_distance:
                closest_employee_dist = emp[0]
                old_distance = distance
            if time < old_time:
                closest_employee_time = emp[0]
                old_time = time

        sql = "UPDATE stores " \
              "SET closest_employee_dist=" + str(closest_employee_dist) + " " \
              "WHERE store_id=" + str(store)
        cur.execute(sql)
        conn.commit()
        sql = "UPDATE stores " \
              "SET closest_employee_time=" + str(closest_employee_time) + " " \
              "WHERE store_id=" + str(store)
        cur.execute(sql)
        conn.commit()


# Updates the stores table.
def assign_closest_reps():
    # loop through stores
    for store in get_all_store_info():
        closest_employee_dist = None
        closest_employee_time = None
        old_distance = 999999999999999
        old_time = 9999999999999999
        # loop through employees
        for emp in get_all_employee_addresses():
            emp_address = emp[2]
            store_address = store[3]
            data = calculate_distance.get_distance(emp_address, store_address)
            distance = data["rows"][0]["elements"][0]["distance"]["value"]
            time = data["rows"][0]["elements"][0]['duration']["value"]
            if distance < old_distance:
                closest_employee_dist = emp[0]
                old_distance = distance
            if time < old_time:
                closest_employee_time = emp[0]
                old_time = time

        sql = "UPDATE stores " \
              "SET closest_employee_dist=" + str(closest_employee_dist) + " " \
              "WHERE store_id=" + str(store[0])
        cur.execute(sql)
        conn.commit()
        sql = "UPDATE stores " \
              "SET closest_employee_time=" + str(closest_employee_time) + " " \
              "WHERE store_id=" + str(store[0])
        cur.execute(sql)
        conn.commit()


def is_rep_qualified(rep, job):
    return rep >= job


def assign_rep_to_job(rep, job):
    sql = "UPDATE jobs SET assigned_employee=" + str(rep) + " WHERE job_id=" + str(job)
    cur.execute(sql)
    conn.commit()


def assign_temp_rep_to_job(rep, job):
    sql = "UPDATE jobs SET temp_employee=" + str(rep) + " WHERE job_id=" + str(job)
    cur.execute(sql)
    conn.commit()


def verify_new_store(retailer_id, number):
    new_store = True
    sql = "SELECT number, retailer FROM stores WHERE retailer=" + str(retailer_id) + " AND number=" + str(number)
    results = cur.execute(sql)
    if results:
        new_store = False
    return new_store


def add_store(retailer, number, add_num, add_st, city, state, zip_code):
    sql = "SELECT id FROM retailers WHERE id=" + str(retailer)
    cur.execute(sql)
    retailer_id = cur.fetchone()
    if retailer_id:
        if verify_new_store(retailer_id[0], number):
            sql = "INSERT INTO stores (retailer, number, address_num, street, city, state, zip)" \
                " VALUES(" + str(retailer_id[0]) + ", " + str(number) + ", " + str(add_num) + ", " \
                "'" + add_st + "', '" + city + "', " \
                "'" + state + "', " + str(zip_code) + ")"
            cur.execute(sql)
            conn.commit()
            sql = "SELECT store_id FROM stores WHERE number=" + str(number) + " AND retailer=" + str(retailer_id[0])
            cur.execute(sql)
            result = cur.fetchone()
            result2 = result  # have to add this because using result[0] below pops the value from the sql query
            set_closest_rep_data_store(result[0])
            assign_closest_reps_to_store(result2[0])
            write_to_json('stores')
            return True
        else:
            return False
    else:
        return False


def verify_new_employee(first_name, last_name, email):
    new_hire = True
    sql = "SELECT first_name, last_name, email FROM employees WHERE first_name='" + re.escape(first_name) + "' " \
          "AND last_name='" + last_name + "' AND email='" + email + "'"
    results = cur.execute(sql)
    if results:
        new_hire = False
    return new_hire


def add_employee(first_name, last_name, add_num, street, city, state, zip_code, phone, email, work_level, hire_date):
    if verify_new_employee(first_name, last_name, email):
        sql = "INSERT INTO employees (first_name, last_name, address_num, street, city, state, zip," \
            " phone, email, work_level, hire_date)" \
            " VALUES ('" + re.escape(first_name) + "', '" + re.escape(last_name) + "', " + str(add_num) + ", '" + re.escape(street) + "', " \
            "'" + re.escape(city) + "', '" + state + "', " + str(zip_code) + ", " + str(phone) + ", '" + email + "', " \
            + str(work_level) + ", '" + date.strftime(hire_date, '%Y-%m-%d') + "')"
        cur.execute(sql)
        conn.commit()
        sql = "SELECT employee_id FROM employees WHERE email='" + email + "'"
        cur.execute(sql)
        result = cur.fetchone()
        set_closest_rep_data_emp(result[0])
        write_to_json('employees')
        return True
    else:
        return False


def verify_new_retailer(name):
    new_retailer = True
    sql = "SELECT name from retailers WHERE name='" + re.escape(name) + "'"
    results = cur.execute(sql)
    if results:
        new_retailer = False
    return new_retailer


def add_retailer(name):
    if verify_new_retailer(name):
        sql = "INSERT INTO retailers (name) VALUES ('" + re.escape(name) + "')"
        cur.execute(sql)
        conn.commit()
        write_to_json('retailers')
        return True
    else:
        return False


def verify_new_client(name):
    new_client = True
    sql = "SELECT name FROM clients WHERE name='" + re.escape(name) + "'"
    results = cur.execute(sql)
    if results:
        new_client = False
    return new_client


def add_client(name, description):
    if verify_new_client(name):
        sql = "INSERT INTO clients (name, description) VALUES ('" + re.escape(name) + "', '" + re.escape(description) + "')"
        cur.execute(sql)
        conn.commit()
        write_to_json('clients')
        return True
    else:
        return False


def add_job(client, store, lvl_req, start_date, end_date):
    sql = "SELECT closest_employee_time, closest_employee_dist FROM stores WHERE store_id=" + str(store)
    cur.execute(sql)
    data = cur.fetchone()
    sql = "INSERT INTO jobs (client_id, store_id, required_level, closest_qual_t_emp, " \
        "closest_qual_d_emp, start_date, end_date) VALUES (" \
        "" + str(client) + ", " + str(store) + ", " + str(lvl_req) + ", " + str(data[0]) + ", " \
        "" + str(data[1]) + ", " \
        "'" + date.strftime(start_date, '%Y-%m-%d') + "', '" + date.strftime(end_date, '%Y-%m-%d') + "')"
    cur.execute(sql)
    conn.commit()
    write_to_json('jobs')


def optimize_job_assignment():
    for job in get_all_jobs():
        old_distance = 9999999999999999
        old_time = 9999999999999999
        for emp in get_all_employee_addresses():
            if is_rep_qualified(emp[3], job[3]):
                data = calculate_distance.get_distance(emp[2], str(get_store_address(job[2])))
                distance = data["rows"][0]["elements"][0]["distance"]["value"]
                time = data["rows"][0]["elements"][0]['duration']["value"]
                if distance < old_distance:
                    closest_employee_dist = emp[0]
                    old_distance = distance
                if time < old_time:
                    closest_employee_time = emp[0]
                    old_time = time
        if closest_employee_time:
            sql = "UPDATE jobs SET closest_qual_t_emp=" + str(closest_employee_time) + " WHERE job_id=" + str(job[0])
            cur.execute(sql)
            conn.commit()
        if closest_employee_dist:
            sql = "UPDATE jobs SET closest_qual_d_emp=" + str(closest_employee_dist) + " WHERE job_id=" + str(job[0])
            cur.execute(sql)
            conn.commit()
    write_to_json('jobs')


def set_dt_for_store(retailer, num):
    # retailer = get_retailer_id(name)
    sql = "SELECT store_id FROM stores WHERE retailer=" + str(retailer) + " AND number=" + str(num)
    cur.execute(sql)
    store_id = cur.fetchone()
    set_closest_rep_data_store(store_id[0])


def write_to_json(name):
    if name == 'retailers':
        retailers_array = []
        for r in get_all_retailers():
            retailer = {
                'id': r[0],
                'name': r[1],
            }
            retailers_array.append(retailer)
        write_to_file = open('static/data/retailers.json', 'w')
        json.dump(retailers_array, write_to_file)
    elif name == 'employees':
        emp_array = []
        for emp in get_all_employee_addresses():
            employee = {
                'id_num': emp[0],
                'name': emp[1],
                'address': emp[2],
                'work_level': emp[3],
            }
            emp_array.append(employee)
        write_to_file = open('static/data/employees.json', 'w')
        json.dump(emp_array, write_to_file)
    elif name == 'stores':
        store_array = []
        for stores in get_all_store_info():
            sql = "SELECT name FROM retailers WHERE id=" + str(stores[1])
            cur.execute(sql)
            retailer = cur.fetchone()
            store = {
                'id_num': stores[0],
                'retailer': {'id': stores[1], 'name': retailer[0]},
                'store_num': stores[2],
                'address': stores[3],
            }
            store_array.append(store)
        write_to_file = open('static/data/stores.json', 'w')
        json.dump(store_array, write_to_file)
    elif name == 'clients':
        clients_array = []
        for c in get_all_clients():
            client = {
                'id': c[0],
                'name': c[1],
            }
            clients_array.append(client)
        write_to_file = open('static/data/clients.json', 'w')
        json.dump(clients_array, write_to_file)
    elif name == 'jobs':
        jobs_array = []
        for j in get_all_jobs():
            sql = "SELECT retailer FROM stores WHERE store_id=" + str(j[2])
            cur.execute(sql)
            retailer = cur.fetchone()
            sql = "SELECT name FROM retailers WHERE id=" + str(retailer[0])
            cur.execute(sql)
            retailer = cur.fetchone()
            sql = "SELECT name FROM clients WHERE client_id=" + str(j[1])
            cur.execute(sql)
            client = cur.fetchone()
            sql = "SELECT closest_qual_d_emp, closest_qual_t_emp, assigned_employee, temp_employee FROM jobs" \
                  " WHERE job_id=" + str(j[0])
            cur.execute(sql)
            assigned = cur.fetchone()
            job = {
                'values': {
                    'job_id': j[0],
                    'client_id': j[1],
                    'store_id': j[2],
                    'required_level': j[3]
                },
                'names': {
                    'store_name': retailer[0],
                    'client': client[0]
                },
                'assigned_reps': {
                    'closest_distance': assigned[0],
                    'closest_time': assigned[1],
                    'assigned': assigned[2],
                    'temp': assigned[3]
                }
            }
            jobs_array.append(job)
        write_to_file = open('static/data/jobs.json', 'w')
        json.dump(jobs_array, write_to_file)


def main():
    assign_closest_reps()
    write_to_json('retailers')
    write_to_json('clients')
    write_to_json('stores')
    write_to_json('employees')
    write_to_json('jobs')
    print("Data entered")


if __name__ == "__main__":
    main()
