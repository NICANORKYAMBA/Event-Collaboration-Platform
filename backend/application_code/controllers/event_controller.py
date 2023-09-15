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
from application_code import db
from application_code.models.event import Event
from application_code.controllers.auth_controller import get_user


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
    Get all events
    """
    try:
        events = Event.query.all()

        if events:
            events_list = [event.serialize() for event in events]
            return jsonify({
                'message': 'All events retrieved successfully.',
                'events': events_list}), 200
        return jsonify({'message': 'No events found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


def get_event(event_id):
    """
    Get event by id
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


def delete_event(event_id):
    """
    Delete event by id
    """
    try:
        event = Event.query.get(event_id)

        if event:
            db.session.delete(event)
            db.session.commit()
            return jsonify({'message': 'Event deleted successfully'}), 200
        return jsonify({'message': 'Event not found'}), 404

    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500


def update_event(event_id):
    """
    Update event by id
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
            return jsonify({'message': 'Event updated successfully'}), 200
        return jsonify({'message': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500
