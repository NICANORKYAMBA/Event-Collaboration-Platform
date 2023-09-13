#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from application_code import db
from datetime import datetime
from application_code.models.event_collaborator import EventCollaborator


class Event(db.Model):
    """
    Defines Events model
    """
    __tablename__ = 'events'

    event_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    organizer_id = db.Column(db.String(36),
                             db.ForeignKey('users.user_id'),
                             nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Define a many to one relationship with users (organizer)
    organizer = db.relationship('User', back_populates='events')
    collaborators = db.relationship(
        'EventCollaborator', back_populates='event')
    tickets = db.relationship('Ticket', back_populates='event')
    rsvps = db.relationship('RSVP', back_populates='event')
    comments = db.relationship('EventComment', back_populates='event')
    ratings = db.relationship('EventRating', back_populates='event')

    def __init__(self,
                 event_name,
                 event_date,
                 event_time,
                 location,
                 description,
                 organizer_id):
        """
        Initialize the event model
        """
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.location = location
        self.description = description
        self.organizer_id = organizer_id
