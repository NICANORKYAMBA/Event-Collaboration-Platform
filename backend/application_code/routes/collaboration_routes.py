#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 16:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from application_code.controllers.collaborator_controller import (
    get_collaborators,
    create_collaborator,
    update_collaborator,
    delete_collaborator,
)

collaborators_bp = Blueprint('collaborators_bp', __name__, url_prefix='/api/v1/collaborators')


@collaborators_bp.route('/list/<int:event_id>',
                        methods=['GET'],
                        strict_slashes=False,
                        endpoint='/list/<int:event_id>')
@jwt_required
def list_collaborators(event_id):
    """
    List all collaborators to an event
    """
    return get_collaborators(event_id)


@collaborators_bp.route('/create/<int:event_id>',
                        methods=['POST'],
                        strict_slashes=False,
                        endpoint='/create/<int:event_id>')
@jwt_required
def add_collaborator(event_id):
    """
    Create and add a collaborator to an event
    """
    return create_collaborator(event_id)


@collaborators_bp.route('/update/<int:event_id>',
                        methods=['PUT'],
                        strict_slashes=False,
                        endpoint='/update/<int:event_id>')
@jwt_required
def modify_collaborator(event_id):
    """
    Update a collaborator for an event
    """
    return update_collaborator(event_id)


@collaborators_bp.route('/delete/<int:event_id>',
                        methods=['DELETE'],
                        strict_slashes=False,
                        endpoint='/delete/<int:event_id>')
@jwt_required
def remove_collaborator(event_id):
    """
    Remove a collaborator from an event
    """
    return delete_collaborator(event_id)
