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

def verify_new_part(client, description):
    return

def add_new_part(part_number, client, description, pic_location):
    if verify_new_part(client, description):
        sql = "INSERT INTO parts (part_number, client, description, pic_location) " \
        "VALUES (" + part_number + ", " + client + ", " + description + ", " + pic_location + ")"
        cur.execute(sql)
        conn.commit()
        return True
    else:
        return False
    # def add_client(name, description):
    # if verify_new_client(name):
    #     sql = "INSERT INTO clients (name, description) VALUES ('" + re.escape(name) + "', '" + re.escape(description) + "')"
    #     cur.execute(sql)
    #     conn.commit()
    #     write_to_json('clients')
    #     return True
    # else:
    #     return False

def new_part_order():
    return

def place_part():
    return

def get_file_name():
    return "../static/parts_images/solo2.jpg"