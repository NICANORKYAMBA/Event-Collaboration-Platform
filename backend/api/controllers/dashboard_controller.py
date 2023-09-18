#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  15 13:00:00 2023

@Author: Nicanor Kyamba

@brief: Dashboard controller
"""
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from api import db
from api.models.user import User
from api.models.event import Event
from api.models.event_collaborator import EventCollaborator
from api.controllers.auth_controller import get_user


def get_user_dashboard():
    """
    Get user dashboard data, including owned events and
    collaborated events

    Args:
        user_id (int): User id
    """
    try:
        user_id = get_jwt_identity()
        user = get_user(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        owned_events = Event.query.filter_by(organizer_id=user_id).all()

        if not owned_events:
            return jsonify({'message': 'No owned events'}), 404

        collaborated_events = EventCollaborator.query.filter_by(
            user_id=user_id).all()

        if not collaborated_events:
            return jsonify({'message': 'No collaborated events'}), 404

        owned_event_data = [event.serialize() for event in owned_events]
        collaborated_event_data = [
                collaborator.event.serialize() for collaborator in collaborated_events]

        return jsonify({
            'user_name': user.user_name,
            'owned_events': owned_event_data,
            'collaborated_events': collaborated_event_data
        }), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
