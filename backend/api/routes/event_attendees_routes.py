#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  27 20:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from api.controllers.event_attendee_controller import (
        add_attendee,
        get_event_attendees,
        delete_attendee,
        get_attendee
        )

event_attendee_bp = Blueprint(
        'event_attendee_bp',
        __name__,
        url_prefix='/api/v1/event-attendees')


@event_attendee_bp.route(
        '/<uuid:event_id>/add',
        methods=['POST'],
        strict_slashes=False,
        endpoint='add_attendee')
@jwt_required()
def add_attendee_to_event(event_id):
    """
    Add an attendee to an event
    """
    return add_attendee(event_id)


@event_attendee_bp.route(
        '/<uuid:event_id>/attendees',
        methods=['GET'],
        strict_slashes=False,
        endpoint='get_event_attendees')
@jwt_required()
def get_attendees_for_event(event_id):
    """
    Get a list of attendees for an event
    """
    return get_event_attendees(event_id)


@event_attendee_bp.route(
        '/<uuid:event_id>/attendees/<uuid:attendee_id>',
        methods=['DELETE'],
        strict_slashes=False,
        endpoint='delete_attendee')
@jwt_required()
def delete_attendee_from_event(event_id, attendee_id):
    """
    Delete an attendee from an event
    """
    return delete_attendee(event_id, attendee_id)


@event_attendee_bp.route(
        '/<uuid:event_id>/attendees/<uuid:attendee_id>',
        methods=['GET'],
        strict_slashes=False,
        endpoint='get_attendee')
@jwt_required()
def get_single_attendee_for_event(event_id, attendee_id):
    """
    Get an attendee from an event
    """
    return get_attendee(event_id, attendee_id)
