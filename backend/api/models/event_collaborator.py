#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from api import db
from datetime import datetime


class EventCollaborator(db.Model):
    """
    Defines Event Collaborator model
    """
    __tablename__ = 'event_collaborators'

    collaborator_id = db.Column(db.String(255),
                                default=lambda: str(uuid.uuid4()),
                                primary_key=True)
    event_id = db.Column(db.String(255),
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    user_id = db.Column(db.String(255),
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    role = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define many to one relationship with events and users
    event = db.relationship('Event', back_populates='collaborators')
    user = db.relationship('User', back_populates='collaborations')

    def __init__(self, event_id, user_id, role):
        """
        Initialize the event collaborator model

        Args:
            event_id (str): event id
            user_id (str): user id
            role (str): role
        """
        self.event_id = event_id
        self.user_id = user_id
        self.role = role

    def serialize(self):
        """
        Serialize the event collaborator model
        """
        return {
            'collaborator_id': self.collaborator_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'role': self.role
        }
