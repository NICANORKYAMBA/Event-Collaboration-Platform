#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  08 13:00:00 2023

@author: Nicanor Kyamba
"""
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

load_dotenv()

from api import create_app, db

app = create_app()

CORS(app, resources={r'/api/*': {'origins': 'http://localhost:8000'}}, supports_credentials=True)

migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True)
