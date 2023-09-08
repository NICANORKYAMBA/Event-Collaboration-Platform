#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 12:00:00 2023

@Author: Nicanor Kyamba
"""
import os


class Config:
    """
    Set Flask configuration vars from .env file
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@localhost/{}'.format(
        os.environ.get('DB_USER'),
        os.environ.get('DB_PASSWORD'),
        os.environ.get('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
