#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  01 14:00:00 2023

@Author: Nicanor Kyamba
"""
import os
import jwt
from functools import wraps
from flask import request, jsonify, current_app
from api.models.user import User

SECRET_KEY = os.environ.get('SECRET_KEY')


def jwt_required(func):
    """
    Decorator to check for a valid JWT token

    Args:
        func (function): function to be decorated
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        full_token = request.headers.get('Authorization')

        token = full_token.replace("Bearer ", "")

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

            if not data:
                return jsonify({'message': 'Token is invalid'}), 401

            current_user = User.query.filter_by(user_id=data['user_id']).first()

            request.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return func(current_user, *args, **kwargs)

    return decorated
