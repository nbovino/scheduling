#!/usr/bin/env python
from __future__ import print_function

import calculate_distance
import db_connect
import json
import pymysql
import re
from datetime import *
from dateutil.parser import parse
import os

conn = db_connect.connect_to_db()
cur = conn.cursor()

def verify_new_part(client, part_number):
    new_part = True
    sql = "SELECT client, part_number FROM parts WHERE client=" + str(client) + " " \
          "AND part_number=" + str(part_number)
    results = cur.execute(sql)
    if results:
        new_part = False
    return new_part

def add_new_part(part_number, client, description, pic_location):
    if verify_new_part(client, part_number):
        sql = "INSERT INTO parts (part_number, client, description, pic_location)" \
            " VALUES (" + str(part_number) + ", " + str(client) + ", " + "'" + re.escape(description) + "', '" + re.escape(pic_location) + "')"
        cur.execute(sql)
        conn.commit()
        write_to_json('part')
        return True
    else:
        return False

def get_all_parts(client=None):
    sql = "SELECT id, part_number, client, description, pic_location FROM parts"
    if client:
        sql += " WHERE client =" + str(client)
    cur.execute(sql)
    return cur.fetchall()

def get_all_parts_simple():
    sql = "SELECT id, description FROM parts"
    cur.execute(sql)
    return cur.fetchall()

def verify_new_part_order(part_id, store_id):
    new_order = True
    sql = "SELECT order_id FROM parts_orders WHERE part_id=" + str(part_id) + " AND store_id=" + str(store_id) + " " \
          "AND placed_date=NULL"
    results = cur.execute(sql)
    if results:
        new_order = False
    return new_order

def new_part_order(ordered_by, client, part_id, store_id, order_date):
    if verify_new_part_order(part_id, store_id):
        sql = "INSERT INTO parts_orders (ordered_by, client, part_id, store_id, order_date)" \
            " VALUES (" + str(ordered_by) + ", " + str(client) + ", " + "'" + str(part_id) + "'," \
            " '" + str(store_id) + "', '" + date.strftime(order_date, '%Y-%m-%d') + "')"
        cur.execute(sql)
        conn.commit()
        write_to_json('order')
        return True
    else:
        return False

def get_all_orders():
    sql = "SELECT order_id, ordered_by, client, part_id, store_id, order_date, placed_date FROM parts_orders"
    # if client:
    #     sql += " WHERE client =" + str(client)
    cur.execute(sql)
    return cur.fetchall()

def place_part():
    return

def get_file_name():
    return "../static/parts_images/solo2.jpg"

def write_to_json(name):
    # TODO: part and order json objects
    if name == 'part':
        parts_array = []
        for p in get_all_parts():
            retailer = {
                'id': p[0],
                'part_number': p[1],
                'client': p[2],
                'description': p[3],
                'pic_location': p[4]
            }
            parts_array.append(retailer)
        write_to_file = open('static/data/parts.json', 'w')
        json.dump(parts_array, write_to_file)
    elif name == 'order':
        order_array = []
        for o in get_all_orders():
            if o[6]:
                placed = date.strftime(o[6], '%Y-%m-%d')
            else:
                placed = 'NULL'
            order = {
                'order_id': o[0],
                'ordered_by': o[1],
                'client': o[2],
                'part_id': o[3],
                'store_id': o[4],
                'order_date': date.strftime(o[5], '%Y-%m-%d'),
                'placed_date': placed
            }
            order_array.append(order)
        write_to_file = open('static/data/orders.json', 'w')
        json.dump(order_array, write_to_file)


    # elif name == 'stores':
    #     store_array = []
    #     for stores in get_all_store_info():
    #         sql = "SELECT name FROM retailers WHERE id=" + str(stores[1])
    #         cur.execute(sql)
    #         retailer = cur.fetchone()
    #         store = {
    #             'id_num': stores[0],
    #             'retailer': {'id': stores[1], 'name': retailer[0]},
    #             'store_num': stores[2],
    #             'address': stores[3],
    #         }
    #         store_array.append(store)
    #     write_to_file = open('static/data/stores.json', 'w')
    #     json.dump(store_array, write_to_file)
    # elif name == 'clients':
    #     clients_array = []
    #     for c in get_all_clients():
    #         client = {
    #             'id': c[0],
    #             'name': c[1],
    #         }
    #         clients_array.append(client)
    #     write_to_file = open('static/data/clients.json', 'w')
    #     json.dump(clients_array, write_to_file)
    # elif name == 'jobs':
    #     jobs_array = []
    #     for j in get_all_jobs():
    #         sql = "SELECT retailer FROM stores WHERE store_id=" + str(j[2])
    #         cur.execute(sql)
    #         retailer = cur.fetchone()
    #         sql = "SELECT name FROM retailers WHERE id=" + str(retailer[0])
    #         cur.execute(sql)
    #         retailer = cur.fetchone()
    #         sql = "SELECT name FROM clients WHERE client_id=" + str(j[1])
    #         cur.execute(sql)
    #         client = cur.fetchone()
    #         sql = "SELECT closest_qual_d_emp, closest_qual_t_emp, assigned_employee, temp_employee FROM jobs" \
    #               " WHERE job_id=" + str(j[0])
    #         cur.execute(sql)
    #         assigned = cur.fetchone()
    #         job = {
    #             'values': {
    #                 'job_id': j[0],
    #                 'client_id': j[1],
    #                 'store_id': j[2],
    #                 'required_level': j[3]
    #             },
    #             'names': {
    #                 'store_name': retailer[0],
    #                 'client': client[0]
    #             },
    #             'assigned_reps': {
    #                 'closest_distance': assigned[0],
    #                 'closest_time': assigned[1],
    #                 'assigned': assigned[2],
    #                 'temp': assigned[3]
    #             }
    #         }
    #         jobs_array.append(job)
    #     write_to_file = open('static/data/jobs.json', 'w')
    #     json.dump(jobs_array, write_to_file)