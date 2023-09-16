#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 16:00:00 2023

@Author: Nicanor Kyamba
"""
from flask_jwt_extended import jwt_required
from flask import Blueprint
from application_code.controllers.rating_controller import (
    create_rating,
    get_ratings,
    get_rating,
    update_rating,
    delete_rating,
)


rating_bp = Blueprint('rating_bp', __name__, url_prefix='/api/v1/ratings')


@rating_bp.route('/create/<uuid:event_id>',
                 methods=['POST'],
                 strict_slashes=False)
@jwt_required()
def create_event_rating(event_id):
    """
    Create a rating for an event
    """
    return create_rating(event_id)


@rating_bp.route('/<uuid:event_id>',
                 methods=['GET'],
                 strict_slashes=False)
@jwt_required()
def get_event_ratings(event_id):
    """
    Get all ratings for an event
    """
    return get_ratings(event_id)


@rating_bp.route('/<uuid:event_id>/<uuid:rating_id>',
                 methods=['GET'],
                 strict_slashes=False)
@jwt_required()
def get_event_rating(event_id, rating_id):
    """
    Get a rating for an event
    """
    return get_rating(event_id, rating_id)


@rating_bp.route('/update/<uuid:event_id>/<uuid:rating_id>',
                 methods=['PUT'],
                 strict_slashes=False)
@jwt_required()
def update_event_rating(event_id, rating_id):
    """
    Update a rating for an event
    """
    return update_rating(event_id, rating_id)


@rating_bp.route('/delete/<uuid:event_id>/<uuid:rating_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@jwt_required()
def delete_event_rating(event_id, rating_id):
    """
    Delete a rating for an event
    """
    return delete_rating(event_id, rating_id)
