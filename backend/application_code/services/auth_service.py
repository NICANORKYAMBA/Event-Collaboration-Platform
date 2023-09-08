#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  01 14:00:00 2023

@Author: Nicanor Kyamba
"""
import jwt
from application_code import db
from application_code.models.user import User

def generate_token(user_id):
    """
    Generate a JWT token for a user

    Args:
        user_id (int): User's ID

    Returns:
        str: JWT token
    """
    payload = {'user_id': user_id}
    secret_key = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token.decode('UTF-8')
