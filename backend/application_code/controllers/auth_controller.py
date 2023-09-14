#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  01 14:00:00 2023

@Author: Nicanor Kyamba
"""
import os
import jwt
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask import request, jsonify, current_app
from application_code import db
from application_code.models.user import User

bcrypt = Bcrypt()
SECRET_KEY = os.environ.get('SECRET_KEY')


def register_user():
    """
    Create a new user and add to the database
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        valid = validate_email(data['email'])
        data['email'] = valid.email

        hashed_password = bcrypt.generate_password_hash(
            data['password'].encode('utf-8'),
            current_app.config.get('SECRET_KEY')
        ).decode('utf-8')

        new_user = User(
                username=data['username'],
                email=data['email'],
                password=hashed_password
            )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'User created successfully',
            'user_id': new_user.user_id}), 201
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email address'}), 400
    except IntegrityError:
        return jsonify({'message': 'Email address already in use'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


def login_user():
    """
    Login a user and return a JWT token
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        user = User.query.filter_by(email=data['email']).first()

        if user and 'password' in data:
            provided_password = data['password']

            if bcrypt.check_password_hash(user.password, provided_password):
                acess_token = create_access_token(identity=user.user_id)
                return jsonify({'message': 'User logged in successfully',
                                'token': acess_token}), 200

        return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


def list_users():
    """
    List all users in the database
    """
    try:
        users = User.query.all()

        if users:
            user_list = [
                {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email
                } for user in users
            ]
            return jsonify({'users': user_list}), 200
        else:
            return jsonify({'message': 'No users found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


def get_user(user_id):
    """
    Get a user by user_id
    """
    try:
        user = User.query.filter_by(user_id=user_id).first()

        if user:
            user_info = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email
            }
            return jsonify({'user': user_info}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


def update_user(user_id):
    """
    Update user by their id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        valid = validate_email(data['email'])
        data['email'] = valid.email

        hashed_password = bcrypt.generate_password_hash(
            data['password'].encode('utf-8'),
            current_app.config.get('SECRET_KEY')
        ).decode('utf-8')

        user = User.query.filter_by(user_id=user_id).first()

        if user:
            if request.current_user.user_id == user.user_id:
                user.username = data['username']
                user.email = data['email']
                user.password = hashed_password
                db.session.commit()
                return jsonify({
                    'message': 'User updated successfully'
                    }), 200
            else:
                return jsonify({
                    'message': 'Unauthorized'
                    }), 401
        else:
            return jsonify({'message': 'User not found'}), 404
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email address'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


def delete_user(user_id):
    """
    Delete a user by their id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'confirm' not in data or data['confirm'] != 'true':
        return jsonify({
            'message': 'Please confirm that you want to delete the user'}), 400
    try:
        user = User.query.filter_by(user_id=user_id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
