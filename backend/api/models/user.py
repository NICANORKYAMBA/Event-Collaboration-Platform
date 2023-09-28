#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from api import db
from sqlalchemy import CheckConstraint
from api.models.event import Event
from api.models.event_collaborator import EventCollaborator
from api.models.event_comment import EventComment
from api.models.event_rating import EventRating
from api.models.rsvp import RSVP
from api.models.ticket import Ticket


class User(db.Model):
    """
    Defines User model
    """
    __tablename__ = 'users'

    user_id = db.Column(
            db.String(255),
            primary_key=True
            )
    username = db.Column(
            db.String(255),
            nullable=False
            )
    email = db.Column(
            db.String(255),
            unique=True,
            nullable=False
            )
    password = db.Column(
            db.String(255),
            nullable=False
            )
    role = db.Column(
            db.String(255),
            nullable=False,
            server_default='Attendee'
            )
    profile_image = db.Column(
            db.String(255)
            )
    created_at = db.Column(
            db.DateTime,
            default=db.func.current_timestamp()
            )
    updated_at = db.Column(
            db.DateTime,
            default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())

    # Define one to many relationship with events,
    # organizer, attendee, collaborator, rsvp, comment, rating models

    events = db.relationship(
            'Event',
            back_populates='organizer'
            )
    events_registered = db.relationship(
            'UserEvent',
            back_populates='user',
            lazy='dynamic'
            )
    attended_events = db.relationship(
            'EventAttendee',
            back_populates='user',
            lazy='dynamic'
            )
    collaborations = db.relationship(
            'EventCollaborator',
            back_populates='user'
            )
    rsvps = db.relationship(
            'RSVP',
            back_populates='user'
            )
    comments = db.relationship(
            'EventComment',
            back_populates='user'
            )
    ratings = db.relationship(
            'EventRating',
            back_populates='user'
            )

    tickets = db.relationship(
            'Ticket',
            back_populates='user'
            )

    __table_args__ = (
        CheckConstraint(
            'role IN ("Organizer", "Attendee")',
            name='user_role'
        ),
    )

    def __init__(self, username, email, password, role):
        """
        Initialize the user model
        """
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def serialize(self):
        """
        Serialize the user model
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'profile_image': self.profile_image
        }
