#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  01 14:00:00 2023

@Author: Nicanor Kyamba
"""
from application_code.middleware.auth_middleware import jwt_required
from application_code.controllers.auth_controller import (
    register_user,
    login_user,
    list_users,
    get_user,
    update_user,
    delete_user,
)
from flask import Blueprint


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """
    Register a user
    """
    return register_user()


@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Login a user
    """
    return login_user()


@auth_bp.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """
    List all users
    """
    return list_users()


@auth_bp.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_single_user(user_id):
    """
    Get a user by their id
    """
    return get_user(user_id)


@auth_bp.route(
        '/users/<int:user_id>/update',
        methods=['PUT'],
        strict_slashes=False)
@jwt_required
def update_single_user(user_id):
    """
    Update a user by their id
    """
    return update_user(user_id)


@auth_bp.route(
        '/users/<int:user_id>/delete',
        methods=['DELETE'],
        strict_slashes=False)
@jwt_required
def delete_single_user(user_id):
    """
    Delete a user by their id
    """
    return delete_user(user_id)
