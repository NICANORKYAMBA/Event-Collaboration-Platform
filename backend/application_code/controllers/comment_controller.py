#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 13:00:00 2023

@Author: Nicanor Kyamba

@description:
    This is the controller file for the comment module.
"""
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from application_code import db
from application_code.models.event_comment import EventComment
from application_code.models.event import Event
from application_code.controllers.event_controller import get_event
from application_code.controllers.auth_controller import get_user
from application_code.models.user import User


def create_comment(event_id):
    """
    Create a comment on an event

    Args:
        event_id (int): id of the event
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        user_id = get_jwt_identity()
        comment_text = data['comment_text']

        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        new_comment = EventComment(
            user_id=user_id,
            event_id=event_id,
            comment_text=comment_text
        )

        db.session.add(new_comment)
        db.session.commit()

        return jsonify({
            'message': 'Comment created successfully',
            'comment_id': new_comment.comment_id
        }), 201
    except Exception as e:
        return jsonify({
            'message': 'An error occurred creating the comment',
            'error': str(e)
        }), 500


def get_comments(event_id):
    """
    Get all comments for an event

    Args:
        event_id (int): id of the event
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        comments = EventComment.query.filter_by(event_id=event_id).all()

        if not comments:
            return jsonify({
                'message': 'No comments found for this event'
                }), 404

        comment_list = [comment.serialize() for comment in comments]

        return jsonify({
            'message': 'Comments retrieved successfully',
            'comments': comment_list
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the comments',
            'error': str(e)
        }), 500


def get_comment(event_id, comment_id):
    """
    Get a comment on an event

    Args:
        event_id (int): id of the event
        comment_id (int): id of the comment
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        comment = EventComment.query.filter_by(
                event_id=event_id, comment_id=comment_id).first()

        if not comment:
            return jsonify({'message': 'Comment not found'}), 404

        return jsonify({
            'message': 'Comment retrieved successfully',
            'comment': comment.serialize()
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the comment',
            'error': str(e)
        }), 500


def update_comment(event_id, comment_id):
    """
    Update a comment on an event

    Args:
        event_id (int): id of the event
        comment_id (int): id of the comment
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        comment = EventComment.query.filter_by(
                event_id=event_id, comment_id=comment_id).first()

        if not comment:
            return jsonify({'message': 'Comment not found'}), 404

        comment_text = data['comment_text']

        if comment_text:
            comment.comment_text = comment_text

        db.session.commit()

        return jsonify({
            'message': 'Comment updated successfully',
            'comment_id': comment.comment_id
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred updating the comment',
            'error': str(e)
        }), 500


def delete_comment(event_id, comment_id):
    """
    Delete a comment on an event

    Args:
        event_id (int): id of the event
        comment_id (int): id of the comment
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        comment = EventComment.query.filter_by(
                event_id=event_id, comment_id=comment_id).first()

        if comment:
            db.session.delete(comment)
            db.session.commit()

            return jsonify({
                'message': 'Comment deleted successfully',
                'comment_id': comment.comment_id
                }), 200
        return jsonify({'message': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({
            'message': 'An error occurred deleting the comment',
            'error': str(e)
        }), 500
