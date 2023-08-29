#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 14:00:00 2023

@Author: Nicanor Kyamba

Database configuration
"""
from sqlalchemy import create_engine


DATABASE_URL = 'mysql+mysqldb://nicanorkyamba:NICmakya98@localhost:5000/events_collaboration_platform'

engine = create_engine(DATABASE_URL)
