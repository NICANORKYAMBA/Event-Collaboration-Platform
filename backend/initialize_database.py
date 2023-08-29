#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 14:00:00 2023

@Author: Nicanor Kyamba

Script to Initialize database
"""
from app.models import Base
from app.config import engine

Base.metadata.create_all(bind=engine)
