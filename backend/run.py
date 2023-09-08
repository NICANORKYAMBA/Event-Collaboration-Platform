#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  08 13:00:00 2023

@author: Nicanor Kyamba
"""
from dotenv import load_dotenv

load_dotenv()

from application_code import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
