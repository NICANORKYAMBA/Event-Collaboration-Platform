#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  01 13:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy

# Create an SQLAlchemy database instance
db = SQLAlchemy()


def create_app(config_class=Config):
    """
    Create a Flask application using the app factory pattern

    Args:
        config_class (object): Configuration settings class
    """
    app = Flask(__name__)

    # Load configuration settings
    if config_class:
        app.config.from_object(config_class)

    # Initialize SQLAlchemy with the flask app
    db.init_app(app)

    # Import and register blueprints
    from application_code.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
