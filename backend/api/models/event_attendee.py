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


class EventAttendee(db.Model):
    """
    Model for event attendees
    """
    __tablename__ = "event_attendees"

    event_attendee_id = db.Column(
            db.String(255),
            primary_key=True
            )
    event_id = db.Column(
            db.String(255),
            db.ForeignKey("events.event_id"),
            nullable=False
            )
    user_id = db.Column(
            db.String(255),
            db.ForeignKey("users.user_id"),
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
            "User",
            back_populates="attended_events"
            )
    event = db.relationship(
            "Event",
            back_populates="attendees"
            )

    def __init__(self, event_id, user_id):
        """
        Constructor for EventAttendee model
        """
        self.event_attendee_id = str(uuid.uuid4())
        self.event_id = event_id
        self.user_id = user_id

    def serialize(self):
        """
        Serialize EventAttendee model
        """
        attendee_details = {
                'username': self.user.username,
                'email': self.user.email
                }

        return {
                "event_attendee_id": self.event_attendee_id,
                "event_id": self.event_id,
                "user_id": self.user_id,
                "attendee_details": attendee_details,
                "created_at": self.created_at,
                "updated_at": self.updated_at
                }
