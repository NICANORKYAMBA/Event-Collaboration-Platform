#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from application_code import db
from datetime import datetime


class RSVP(db.Model):
    """
    Defines RSVP model
    """
    __tablename__ = 'rsvps'

    rsvp_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    user_id = db.Column(db.String(36),
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    ticket_id = db.Column(db.Integer,
                          db.ForeignKey('tickets.ticket_id'),
                          nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define many to one relationship with events, users and tickets
    event = db.relationship('Event', back_populates='rsvps')
    user = db.relationship('User', back_populates='rsvps')
    ticket = db.relationship('Ticket', back_populates='rsvps')

    def __init__(self, event_id, user_id, ticket_id):
        """
        Initialize the RSVP model

        Args:
                event_id (_type_): _description_
                user_id (_type_): _description_
                ticket_id (_type_): _description_
        """
        self.event_id = event_id
        self.user_id = user_id
        self.ticket_id = ticket_id
