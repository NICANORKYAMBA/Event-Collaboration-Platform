#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  27 19:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from api import db
from api.models.event_attendee import EventAttendee
from api.models.user import User
from api.models.event import Event


def add_attendee(event_id):
    """
    Add an attendee to an event
    """
    try:
        user_id = get_jwt_identity()

        event = Event.query.get(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        existing_attendee = EventAttendee.query.filter_by(
            user_id=user_id, event_id=event_id).first()

        if existing_attendee:
            return jsonify({
                'message': 'User is already an attendee of this event'
                }), 400

        attendee = EventAttendee(
                user_id=user_id, event_id=event_id)
        db.session.add(attendee)
        db.session.commit()

        return jsonify({
            'message': 'User added as an attendee to the event successfully'
            }), 201
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def get_event_attendees(event_id):
    """
    Get a list of attendees for an event
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'message': 'Event not found'
                }), 404

        event_attendees = EventAttendee.query.filter_by(
                event_id=event_id).all()

        if not event_attendees:
            return jsonify({
                'message': 'No attendees found for the event'
                }), 404

        attendees = []
        for event_attendee in event_attendees:
            user = User.query.get(event_attendee.user_id)
            if user:
                attendees.append(user.serialize())

        return jsonify({
            'message': 'Attendees of the event',
            'attendees': attendees
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def delete_attendee(event_id, attendee_id):
    """
    Delete an attendee from an event
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'message': 'Event not found'
                }), 404

        attendee = EventAttendee.query.get(attendee_id)

        if not attendee:
            return jsonify({
                'message': 'Attendee not found'
                }), 404

        db.session.delete(attendee)
        db.session.commit()

        return jsonify({
            'message': 'Attendee deleted successfully'
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def get_attendee(event_id, attendee_id):
    """
    Get an attendee from an event
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'message': 'Event not found'
                }), 404

        attendee = EventAttendee.query.get(attendee_id)

        if not attendee:
            return jsonify({
                'message': 'Attendee not found'
                }), 404

        return jsonify({
            'message': 'Attendee details',
            'attendee': attendee.serialize()
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500
