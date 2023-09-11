#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from application_code import db
from datetime import datetime


class EventCollaborator(db.Model):
    """
    Defines Event Collaborator model
    """
    __tablename__ = 'event_collaborators'

    collaborator_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    role = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define many to one relationship with events and users
    event = db.relationship('Event', back_populates='collaborators')
    user = db.relationship('User', back_populates='collaborations')

    def __init__(self, event_id, user_id, role):
        """
        Initialize the event collaborator model
        """
        self.event_id = event_id
        self.user_id = user_id
        self.role = role
