#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  01 13:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config, TestConfig
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

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Import and register blueprints
    from api.routes.auth_routes import auth_bp
    from api.routes.event_routes import event_bp
    from api.routes.dashboard_routes import dashboard_bp
    from api.routes.collaboration_routes import collaborators_bp
    from api.routes.comments_routes import comments_bp
    from api.routes.ratings_routes import rating_bp
    from api.routes.rsvp_routes import rsvp_bp
    from api.routes.ticket_routes import ticket_bp
    from api.routes.event_attendees_routes import event_attendee_bp
    from api.routes.user_event_routes import user_event_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(collaborators_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(rating_bp)
    app.register_blueprint(rsvp_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(event_attendee_bp)
    app.register_blueprint(user_event_bp)

    return app
