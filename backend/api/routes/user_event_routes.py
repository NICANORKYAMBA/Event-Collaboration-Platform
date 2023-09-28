#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  27 19:30:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.controllers.user_event_controller import (
        register_for_event,
        get_events_registered_for,
        delete_registration_for_event
        )

user_event_bp = Blueprint(
        'user_event_bp',
        __name__,
        url_prefix='/api/v1/user-events')


@user_event_bp.route(
        '/register/<uuid:event_id>',
        methods=['POST'],
        strict_slashes=False,
        endpoint='register_event')
@jwt_required()
def register_user_for_event(event_id):
    """
    Register a user for an event
    """
    return register_for_event(event_id)


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
    return get_events_registered_for()


@user_event_bp.route(
        '/registered-events/<uuid:event_id>',
        methods=['DELETE'],
        strict_slashes=False,
        endpoint='delete_registered_event')
@jwt_required()
def delete_user_registered_event(event_id):
    """
    Delete a user event registration
    """
    return delete_registration_for_event(event_id)
