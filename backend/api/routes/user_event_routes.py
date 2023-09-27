#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  27 19:30:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.controllers.user_event_controller import (
        register_event,
        get_registered_events,
        delete_registered_event,
        get_user_events,
        delete_user_event
        )

user_event_bp = Blueprint(
        'user_event_bp',
        __name__,
        url_prefix='/api/v1/user-events')


@user_event_bp.route(
        '/register',
        methods=['POST'],
        strict_slashes=False,
        endpoint='register_event')
@jwt_required()
def register_user_for_event():
    """
    Register a user for an event
    """
    return register_event()


@user_event_bp.route(
        '/registered-events',
        methods=['GET'],
        strict_slashes=False,
        endpoint='get_registered_events')
@jwt_required()
def get_user_registered_events():
    """
    Get a list of events registered by the user
    """
    return get_registered_events()


@user_event_bp.route(
        '/registered-events',
        methods=['DELETE'],
        strict_slashes=False,
        endpoint='delete_registered_event')
@jwt_required()
def delete_user_registered_event():
    """
    Delete a user event registration
    """
    return delete_registered_event()


@user_event_bp.route(
        '/user-events',
        methods=['GET'],
        strict_slashes=False,
        endpoint='get_user_events')
@jwt_required()
def get_user_events_registered():
    """
    Get a list of events the user is registered for
    """
    return get_user_events()


@user_event_bp.route(
        '/user-events',
        methods=['DELETE'],
        strict_slashes=False,
        endpoint='delete_user_event')
@jwt_required()
def delete_user_event_registered():
    """
    Delete a user event
    """
    return delete_user_event()
