#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

database_uri = 'mysql+mysqldb://nicanorkyamba:NICmakya98@localhost/events_collaboration_platform'
engine = create_engine(database_uri)

try:
    connection = engine.connect()
    print("Database connection successful.")
    connection.close()
except Exception as e:
    print("Error connecting to the database:", str(e))
