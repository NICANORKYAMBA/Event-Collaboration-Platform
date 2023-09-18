#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 16:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from api.controllers.dashboard_controller import get_user_dashboard


dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/api/v1/dashboard')


@dashboard_bp.route('/user',
                    methods=['GET'],
                    strict_slashes=False)
@jwt_required
def get_dashboard_data():
    """
    Get user dashboard data
    """
    return get_user_dashboard()
