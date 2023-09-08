#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from application_code import db


class User(db.Model):
    """
    Defines User model
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    # Define one to many relationship with events
    events = db.relationship('Event', back_populates='organizer')
    collaborations = db.relationship('EventCollaborator', back_populates='user')
    rsvps = db.relationship('RSVP', back_populates='user')
    comments = db.relationship('EventComment', back_populates='user')
    ratings = db.relationship('EventRating', back_populates='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
