#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 16:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from application_code.controllers.rsvp_controller import (
    create_rsvp,
    get_rsvps,
    get_rsvp,
    get_user_rsvps,
    delete_rsvp,
)


rsvp_bp = Blueprint("rsvp_bp", __name__, url_prefix="/api/v1/rsvps")


@rsvp_bp.route('/create/<int:event_id>',
                methods=['POST'],
               strict_slashes=False)
@jwt_required()
def create_event_rsvp(event_id):
    """
    Create a rsvp for an event
    """
    return create_rsvp(event_id)


@rsvp_bp.route('/get/<int:event_id>',
                methods=['GET'],
               strict_slashes=False)
@jwt_required()
def get_event_rsvps(event_id):
    """
    Get all rsvps for an event
    """
    return get_rsvps(event_id)


@rsvp_bp.route('/get/<int:rsvp_id>',
                methods=['GET'],
               strict_slashes=False)
@jwt_required()
def get_single_rsvp(rsvp_id):
    """
    Get a single rsvp
    """
    return get_rsvp(rsvp_id)


@rsvp_bp.route('/user/<int:user_id>',
                methods=['GET'],
               strict_slashes=False)
@jwt_required()
def get_user_rsvps(user_id):
    """
    Get all rsvps for a user
    """
    return get_user_rsvps(user_id)


@rsvp_bp.route('/delete/<int:rsvp_id>',
                methods=['DELETE'],
               strict_slashes=False)
@jwt_required()
def delete_rsvp(rsvp_id):
    """
    Delete a rsvp by its id
    """
    return delete_rsvp(rsvp_id)
