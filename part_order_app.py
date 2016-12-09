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

