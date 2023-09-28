#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from api import db
from datetime import datetime


class RSVP(db.Model):
    """
    Defines RSVP model
    """
    __tablename__ = 'rsvps'

    rsvp_id = db.Column(db.String(255),
                        default=lambda: str(uuid.uuid4()),
                        primary_key=True)
    event_id = db.Column(db.String(255),
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    user_id = db.Column(db.String(255),
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    ticket_id = db.Column(db.String(255),
                          db.ForeignKey('tickets.ticket_id'),
                          nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define many to one relationship with events, users and tickets
    event = db.relationship('Event', back_populates='rsvps')
    user = db.relationship('User', back_populates='rsvps')
    ticket = db.relationship('Ticket', back_populates='rsvps')

    def __init__(self, event_id, user_id, ticket_id):
        """
        Initialize the RSVP model

        Args:
            event_id (str): event id
            user_id (str): user id
            ticket_id (str): ticket id
        """
        self.event_id = event_id
        self.user_id = user_id
        self.ticket_id = ticket_id

    def serialize(self):
        """
        Serialize the RSVP model
        """
        return {
            'rsvp_id': self.rsvp_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'ticket_id': self.ticket_id
        }
