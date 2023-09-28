#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  11 20:00:00 2023

@Author: Nicanor Kyamba
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError
from api import db
from api.models.event import Event
from api.controllers.auth_controller import get_user


def is_organizer(user):
    """
    Check if user is organizer
    """
    return user.role == 'organizer'

def organizer_required(f):
    """
    Check if user is organizer
    """
    @wraps(f)
    def decorated_func(*args, **kwargs):
        """
        Check if user is organizer
        """
        user = get_user(get_jwt_identity())

        if not is_organizer(user):
            return jsonify({
                'message': 'Only Event Organizers can perform this action'
                }), 403
        return f(*args, **kwargs)
    return decorated_func


@organizer_required
def create_event():
    """
    Create a new event and add to the database
    """
    data = request.json

    if not data:
        return jsonify({'message': 'Not input data provided'}), 400

    try:
        organizer_id = get_jwt_identity()
        new_event = Event(
                event_name=data['event_name'],
                event_date=data['event_date'],
                event_time=data['event_time'],
                location=data['location'],
                description=data['description'],
                organizer_id=organizer_id
                )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({'message': 'Event created successfully',
                        'event_id': new_event.event_id}), 201
    except IntegrityError:
        return jsonify({'message': 'Event already exists'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


def get_events():
    """
    Get all events created
    """
    try:
        events = Event.query.all()

        if events:
            events_list = [
                    {
                        'event_id': event.event_id,
                        'organizer_id': event.organizer_id,
                        'event_name': event.event_name,
                        'event_date': event.event_date,
                        'event_time': event.event_time.strftime('%H:%M:%S'),
                        'location': event.location,
                        'description': event.description
                    }
                    for event in events
                ]
            return jsonify({
                'message': 'All events retrieved successfully.',
                'events': events_list}), 200
        return jsonify({'message': 'No events found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


def get_event(event_id):
    """
    Get an event by its event id
    """
    try:
        event = Event.query.get(event_id)

        if event:
            return jsonify({
                'message': 'Event retrieved successfully',
                'event': event.serialize()}), 200
        return jsonify({'message': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


@organizer_required
def get_events_by_user(user_id):
    """
    Get all events created by a specific user by their id
    """
    try:
        events = Event.query.filter_by(organizer_id=user_id).all()

        if events:
            events_list = [
                    {
                        'event_id': event.event_id,
                        'organizer_id': event.organizer_id,
                        'event_name': event.event_name,
                        'event_date': event.event_date,
                        'event_time': event.event_time.strftime('%H:%M:%S'),
                        'location': event.location,
                        'description': event.description
                    }
                    for event in events
                ]
            return jsonify({
                'message': 'All events retrieved successfully.',
                'events': events_list}), 200
        return jsonify({'message': 'No events found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


@organizer_required
def delete_event(event_id):
    """
    Delete event by its event id
    """
    try:
        event = Event.query.get(event_id)

        if event:
            db.session.delete(event)
            db.session.commit()
            return jsonify({'message': 'Event deleted successfully',
                            'event_id': event.event_id}), 200
        return jsonify({'message': 'Event not found'}), 404

    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


@organizer_required
def update_event(event_id):
    """
    Update event by its event id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'Not input data provided'}), 400

    try:
        event = Event.query.get(event_id)

        if event:
            event.event_name = data['event_name']
            event.event_date = data['event_date']
            event.event_time = data['event_time']
            event.location = data['location']
            event.description = data['description']
            db.session.commit()
            return jsonify({'message': 'Event updated successfully',
                            'event_id': event.event_id}), 200
        return jsonify({'message': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500
