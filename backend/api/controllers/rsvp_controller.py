#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from api import db
from api.models.rsvp import RSVP
from api.models.ticket import Ticket
from api.controllers.auth_controller import get_user
from api.controllers.event_controller import get_event


def create_rsvp(event_id):
    """
    Create an RSVP for an event

    Args:
        event_id (int): Event ID
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        user_id = get_jwt_identity()
        ticket_id = data['ticket_id']

        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()

        if not ticket:
            return jsonify({'message': 'Ticket not found'}), 404

        new_rsvp = RSVP(
            event_id=event_id,
            user_id=user_id,
            ticket_id=ticket_id
        )

        db.session.add(new_rsvp)
        db.session.commit()

        return jsonify({
            'message': 'RSVP created successfully',
            'rsvp_id': new_rsvp.rsvp_id
        }), 201
    except Exception as e:
        return jsonify({
            'message': 'An error occurred creating the rsvp',
            'error': str(e)
        }), 500


def get_rsvps(event_id):
    """
    Get all rsvps for an event

    Args:
        event_id (int): Event ID
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        rsvps = RSVP.query.filter_by(event_id=event_id).all()

        if not rsvps:
            return jsonify({'message': 'No rsvps found for this event'}), 404

        rsvp_list = [rsvp.serialize() for rsvp in rsvps]

        return jsonify({
            'message': 'RSVPs retrieved successfully',
            'rsvps': rsvp_list
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the rsvps',
            'error': str(e)
        }), 500


def get_rsvp(rsvp_id):
    """
    Get an RSVP

    Args:
        rsvp_id (int): RSVP ID
    """
    try:
        rsvp = RSVP.query.filter_by(rsvp_id=rsvp_id).first()

        if not rsvp:
            return jsonify({'message': 'RSVP not found'}), 404

        return jsonify({
            'message': 'RSVP retrieved successfully',
            'rsvp': rsvp.serialize()
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the rsvp',
            'error': str(e)
        }), 500


def get_user_rsvps(user_id):
    """
    Get all rsvps for a user

    Args:
        user_id (int): User ID
    """
    try:
        user = get_user(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        rsvps = RSVP.query.filter_by(user_id=user_id).all()

        if not rsvps:
            return jsonify({'message': 'No rsvps found for this user'}), 404

        rsvp_list = [rsvp.serialize() for rsvp in rsvps]

        return jsonify({
            'message': 'RSVPs retrieved successfully',
            'rsvps': rsvp_list
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the rsvps',
            'error': str(e)
        }), 500


def delete_rsvp(rsvp_id):
    """
    Delete an RSVP

    Args:
        rsvp_id (int): RSVP ID
    """
    try:
        rsvp = RSVP.query.filter_by(rsvp_id=rsvp_id).first()

        if not rsvp:
            return jsonify({'message': 'RSVP not found'}), 404

        db.session.delete(rsvp)
        db.session.commit()

        return jsonify({
            'message': 'RSVP deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred deleting the rsvp',
            'error': str(e)
        }), 500
