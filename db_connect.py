#!/usr/bin/env python
from __future__ import print_function

import calculate_distance
import pymysql


def connect_to_db():
    return pymysql.connect(host='localhost',
                           port=8889,
                           user='root',
                           passwd='root',
                           db='BDS_SCHEDULING')


# conn = connect_to_db()
# cur = conn.cursor()
# TRIAL QUERIES TO DB
#
# name_address_sql = "SELECT CONCAT(last_name, ', ', first_name) as full_name, CONCAT(address_num, ' ', street, '. '," \
#                    "city, ', ', state, ' ' , zip) as full_address FROM employees"
# cur.execute(name_address_sql)
# print(cur.execute((name_address_sql)))
# for row in cur:
#     print(row)
#
# store_address_sql = "SELECT name, number, CONCAT(address_num, ' ', street, '. ', city, ', ', state, ' ', zip) as store_address FROM stores"
#
# cur.execute(store_address_sql)
# for row in cur:
#     print(row[0] + ' ' + row[2])
#
# cur.close()
# conn.close()

