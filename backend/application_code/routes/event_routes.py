#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  13 17:00:00 2023

@Author: Firstname Lastname

@description:
    This is the event routes file.
"""
from flask import Blueprint
from application_code.middleware.auth_middleware import jwt_required
from application_code.controllers.event_controller import (
    create_event,
    get_event,
    get_events,
    update_event,
    delete_event,
)


event_bp = Blueprint("event_bp", __name__, url_prefix="/api/v1/events")


@event_bp.route("/new_event",
                methods=["POST"],
                strict_slashes=False)
@jwt_required
def create_event_route(current_user):
    """
    Create a new event
    """
    return create_event()


@event_bp.route("/get_event/<int:event_id>",
                methods=["GET"],
                strict_slashes=False)
@jwt_required
def get_event_route(current_user, event_id):
    """
    Get an event by id
    """
    return get_event(event_id)


@event_bp.route("/get_events",
                methods=["GET"],
                strict_slashes=False)
@jwt_required
def get_events_route(current_user):
    """
    Get all events
    """
    return get_events()


@event_bp.route("/update_event/<int:event_id>",
                methods=["PUT"],
                strict_slashes=False)
@jwt_required
def update_event_route(current_user, event_id):
    """
    Update an event
    """
    return update_event(event_id)


@event_bp.route("/delete_event/<int:event_id>",
                methods=["DELETE"],
                strict_slashes=False)
@jwt_required
def delete_event_route(current_user, event_id):
    """
    Delete an event
    """
    return delete_event(event_id)
