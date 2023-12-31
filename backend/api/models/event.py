#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from api import db
from datetime import datetime
from api.models.event_collaborator import EventCollaborator


class Event(db.Model):
    """
    Defines Events model
    """
    __tablename__ = 'events'

    event_id = db.Column(
            db.String(255),
            primary_key=True
            )
    event_name = db.Column(
            db.String(255),
            nullable=False
            )
    event_date = db.Column(
            db.Date,
            nullable=False
            )
    event_time = db.Column(
            db.Time,
            nullable=False
            )
    location = db.Column(
            db.String(255),
            nullable=False
            )
    description = db.Column(db.Text)
    organizer_id = db.Column(
            db.String(255),
            db.ForeignKey('users.user_id'),
            nullable=False
            )
    created_at = db.Column(
            db.DateTime,
            default=db.func.current_timestamp()
            )
    updated_at = db.Column(
            db.DateTime,
            default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp()
            )

    # Define a many to one relationship with users (organizer)
    registered_users = db.relationship(
            'UserEvent',
            back_populates='event',
            lazy='dynamic'
            )
    attendees = db.relationship(
            'EventAttendee',
            back_populates='event',
            lazy='dynamic'
            )
    organizer = db.relationship(
            'User',
            back_populates='events',
            )
    collaborators = db.relationship(
            'EventCollaborator',
            back_populates='event'
            )
    tickets = db.relationship(
            'Ticket',
            back_populates='event'
            )
    rsvps = db.relationship(
            'RSVP',
            back_populates='event'
            )
    comments = db.relationship(
            'EventComment',
            back_populates='event'
            )
    ratings = db.relationship(
            'EventRating',
            back_populates='event'
            )

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
        self.event_id = str(uuid.uuid4())
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.location = location
        self.description = description
        self.organizer_id = organizer_id

    def serialize(self):
        """
        Serialize the event
        """
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'event_date': self.event_date.strftime('%Y-%m-%d'),
            'event_time': self.event_time.strftime('%H:%M:%S'),
            'location': self.location,
            'description': self.description,
            'organizer_id': self.organizer_id,
        }
