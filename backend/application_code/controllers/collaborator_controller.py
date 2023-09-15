#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 11:00:00 2023

@Author: Nicanor Kyamba

@description:
    event collaborators controller
"""
from flask import request, jsonify
from application_code import db
from sqlalchemy.exc import IntegrityError
from application_code.controllers.auth_controller import get_user
from application_code.models.event_collaborator import EventCollaborator
from application_code.models.event import Event
from application_code.models.user import User


def get_collaborators(event_id):
    """
    List all collaborators to an event

    Args:
        event_id (int): event id
    """
    try:
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        collaborators = EventCollaborator.query.filter_by(
            event_id=event_id
            ).all()

        if collaborators:
            collaborator_list = []

            for collaborator in collaborators:
                user = User.query.get(collaborator.user_id)
                if user:
                    collaborator_data = {
                        'collaborator_id': collaborator.collaborator_id,
                        'user_id': collaborator.user_id,
                        'role': collaborator.role,
                        'user_name': user.user_name,
                        'user_email': user.user_email,
                    }
                    collaborator_list.append(collaborator_data)

            return jsonify({'collaborators': collaborator_list}), 200

        return jsonify({'message': 'No collaborators found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


def create_collaborator(event_id):
    """
    Create and add a collaborator to an event

    Args:
        event_id (int): event id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        user_id = data['user_id']
        role = data['role']

        event = Event.query.get(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        user = get_user(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        existing_collaborator = EventCollaborator.query.filter_by(
            event_id=event_id,
            user_id=user_id,
            ).first()

        if existing_collaborator:
            return jsonify({
                'message': 'User is already a collaborator in this event'
                }), 400

        organizer_id = get_user().user_id

        if event.organizer_id != organizer_id:
            return jsonify({
                'message': 'Only the event organizer can add collaborators'
                }), 400

        new_collaborator = EventCollaborator(
            event_id=event_id,
            user_id=user_id,
            role=role
        )

        db.session.add(new_collaborator)
        db.session.commit()

        return jsonify({'message': 'Collaborator added successfully',
                        'collaborator_id': new_collaborator.collaborator_id
                        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'message': 'User is already a collaborator in this event'
            }), 400
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def update_collaborator(event_id):
    """
    Update a collaborator to an event

    Args:
        event_id (int): event id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        collaborator_id = data['collaborator_id']

        if not collaborator_id:
            return jsonify({'message': 'Collaborator ID not provided'}), 400

        collaborator = EventCollaborator.query.get(collaborator_id)

        if not collaborator:
            return jsonify({'message': 'Collaborator not found'}), 404

        role = data['role']

        if role is not None:
            collaborator.role = role

        db.session.commit()

        return jsonify({
            'message': 'Collaborator updated successfully'
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)
            }), 500


def delete_collaborator(event_id):
    """
    Remove a collaborator from an event

    Args:
        event_id (int): event id
    """
    data = request.json

    if not data:
        return jsonify({
            'message': 'No input data provided'}), 400

    try:
        collaborator_id = data['collaborator_id']

        if not collaborator_id:
            return jsonify({
                'message': 'Collaborator ID not provided'
                }), 400

        collaborator = EventCollaborator.query.get(collaborator_id)

        if not collaborator:
            return jsonify({'message': 'Collaborator not found'}), 404

        db.session.delete(collaborator)
        db.session.commit()

        return jsonify({
            'message': 'Collaborator removed successfully'
            }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred',
            'error': str(e)}), 500
