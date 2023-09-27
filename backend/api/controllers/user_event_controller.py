#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  27 21:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from api import db
from api.models.user_event import UserEvent
from api.models.user import User
from api.models.event import Event


def register_event():
    """
    Register a user for an event
    """
    try:
        user_id = get_jwt_identity()
        data = request.json

        if not data:
            return jsonify({
                'message': 'No input data provided'
                }), 400

        event_id = data.get('event_id')

        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'message': 'Event not found'
                }), 404

        existing_registration = UserEvent.query.filter_by(
            user_id=user_id, event_id=event_id).first()

        if existing_registration:
            return jsonify({
                'message': 'User is already registered for this event'
                }), 400

        user_event = UserEvent(user_id=user_id, event_id=event_id)
        db.session.add(user_event)
        db.session.commit()

        return jsonify({
            'message': 'User registered for the event successfully'
            }), 201
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def get_registered_events():
    """
    Get a list of events registered by the user
    """
    try:
        user_id = get_jwt_identity()

        user_events = UserEvent.query.filter_by(
                user_id=user_id).all()

        if not user_events:
            return jsonify({
                'message': 'No events registered by the user'
                }), 404

        registered_events = []
        for user_event in user_events:
            event = Event.query.get(user_event.event_id)
            if event:
                registered_events.append(event.serialize())

        return jsonify({
            'message': 'Events registered by the user',
            'events': registered_events
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def delete_registered_event():
    """
    Delete a user event registration
    """
    try:
        user_id = get_jwt_identity()
        data = request.json

        if not data:
            return jsonify({
                'message': 'No input data provided'
                }), 400

        event_id = data.get('event_id')

        event = Event.query.get(event_id)

        if not event:
            return jsonify({
                'message': 'Event not found'
                }), 404

        existing_registration = UserEvent.query.filter_by(
            user_id=user_id, event_id=event_id).first()

        if not existing_registration:
            return jsonify({
                'message': 'User is not registered for this event'
                }), 400

        db.session.delete(existing_registration)
        db.session.commit()

        return jsonify({
            'message': 'User event deleted successfully'
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500

def get_user_events():
    """
    Get a list of events the user is registered for
    """
    try:
        user_id = get_jwt_identity()

        user_events = UserEvent.query.filter_by(user_id=user_id).all()

        if not user_events:
            return jsonify({
                'message': 'No events registered by the user'
                }), 404

        registered_events = []
        for user_event in user_events:
            event = Event.query.get(user_event.event_id)
            if event:
                registered_events.append(event.serialize())

        return jsonify({
            'message': 'Events registered by the user',
            'events': registered_events
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500

def delete_user_event():
    """
    Delete a user event
    """
    try:
        user_id = get_jwt_identity()
        data = request.json

        if not data:
            return jsonify({
                'message': 'No input data provided'
                }), 400

        event_id = data.get('event_id')

        event = Event.query.get(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        existing_registration = UserEvent.query.filter_by(
            user_id=user_id, event_id=event_id).first()

        if not existing_registration:
            return jsonify({
                'message': 'User is not registered for this event'
                }), 400

        db.session.delete(existing_registration)
        db.session.commit()

        return jsonify({
            'message': 'User event deleted successfully'
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)}), 500
