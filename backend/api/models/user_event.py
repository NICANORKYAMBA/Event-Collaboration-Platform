#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  27 19:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from api import db
from api.models.user import User
from api.models.event import Event
from datetime import datetime


class UserEvent(db.Model):
    """
    UserEvent model
    """
    __tablename__ = 'user_events'

    user_event_id = db.Column(
            db.String(255),
            primary_key=True
            )
    event_id = db.Column(
            db.String(255),
            db.ForeignKey('events.event_id'),
            nullable=False
            )
    user_id = db.Column(
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

    # Define relationships with User and Event models
    user = db.relationship(
            'User',
            back_populates='events_registered')
    event = db.relationship(
            'Event',
            back_populates='registered_users')

    def __init__(self, user_id, event_id):
        """
        Initialize UserEvent model
        """
        self.user_event_id = str(uuid.uuid4())
        self.user_id = user_id
        self.event_id = event_id

    def serialize(self):
        """
        Serialize UserEvent model
        """
        event_details = {
                'event_id': self.event.event_id,
                'event_name': self.event.event_name,
                'event_date': self.event.event_date.strftime('%Y-%m-%d'),
                'event_time': self.event.event_time.strftime('%H:%M:%S'),
                'location': self.event.location
                }

        return {
                'user_event_id': self.user_event_id,
                'user_id': self.user_id,
                'event_id': self.event_id,
                'event_details': event_details,
                'created_at': self.created_at,
                'updated_at': self.updated_at
                }
