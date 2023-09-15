#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 16:00:00 2023

@Author: Nicanor Kyamba
"""
from flask_jwt_extended import jwt_required
from flask import Blueprint
from application_code.controllers.comments_controller import (
    create_comment,
    get_comments,
    get_comment,
    update_comment,
    delete_comment
)

comments_bp = Blueprint('comments_bp', __name__, url_prefix='api/v1/comments')


@comments_bp.route('/create/<int:event_id>',
                   methods=['POST'],
                   strict_slashes=False)
@jwt_required
def create_comment(event_id):
    """
    Create a comment for an event
    """
    return create_comment(event_id)


@comments_bp.route('/get/<int:event_id>',
                   methods=['GET'],
                   strict_slashes=False)
@jwt_required
def get_comments(event_id):
    """
    Get all comments for an event
    """
    return get_comments(event_id)


@comments_bp.route('/get/<int:event_id>/<int:comment_id>',
                   methods=['GET'],
                   strict_slashes=False)
@jwt_required
def get_comment(event_id, comment_id):
    """
    Get a comment for an event
    """
    return get_comment(event_id, comment_id)


@comments_bp.route('/update/<int:event_id>/<int:comment_id>',
                   methods=['PUT'],
                   strict_slashes=False)
@jwt_required
def update_comment(event_id, comment_id):
    """
    Update a comment for an event
    """
    return update_comment(event_id, comment_id)


@comments_bp.route('/delete/<int:event_id>/<int:comment_id>',
                   methods=['DELETE'],
                   strict_slashes=False)
@jwt_required
def delete_comment(event_id, comment_id):
    """
    Delete a comment for an event
    """
    return delete_comment(event_id, comment_id)
