#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 16:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from application_code.controllers.ticket_controller import (
    create_ticket,
    get_tickets,
    get_ticket,
    update_ticket,
    delete_ticket,
)


ticket_bp = Blueprint('ticket_bp', __name__, url_prefix='/api/v1/tickets')


@ticket_bp.route('/create/<uuid:event_id>',
                 methods=['POST'],
                 strict_slashes=False)
@jwt_required()
def create_event_ticket(event_id):
    """
    Create a ticket for an event
    """
    return create_ticket(event_id)


@ticket_bp.route('/<uuid:event_id>',
                 methods=['GET'],
                 strict_slashes=False)
@jwt_required()
def get_event_tickets(event_id):
    """
    Get all tickets for an event
    """
    return get_tickets(event_id)


@ticket_bp.route('/<uuid:event_id>/<uuid:ticket_id>',
                 methods=['GET'],
                 strict_slashes=False)
@jwt_required()
def get_event_ticket(event_id, ticket_id):
    """
    Get a ticket for an event
    """
    return get_ticket(event_id, ticket_id)


@ticket_bp.route('/update/<uuid:event_id>/<uuid:ticket_id>',
                 methods=['PUT'],
                 strict_slashes=False)
@jwt_required()
def update_event_ticket(event_id, ticket_id):
    """
    Update a ticket for an event
    """
    return update_ticket(event_id, ticket_id)


@ticket_bp.route('/delete/<uuid:event_id>/<uuid:ticket_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@jwt_required()
def delete_event_ticket(event_id, ticket_id):
    """
    Delete a ticket for an event
    """
    return delete_ticket(event_id, ticket_id)
