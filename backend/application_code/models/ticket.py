#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from application_code import db
from datetime import datetime


class Ticket(db.Model):
    """
    Defines Tickets model
    """
    __tablename__ = 'tickets'

    ticket_id = db.Column(db.String(255),
                          default=lambda: str(uuid.uuid4()),
                          primary_key=True)
    event_id = db.Column(db.String(255),
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    ticket_type = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,
                           default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    # Define many to one relationship with events
    event = db.relationship('Event', back_populates='tickets')
    rsvps = db.relationship('RSVP', back_populates='ticket')

    def __init__(self, event_id, ticket_type, price, quantity_available):
        """
        Initialize the ticket model

        Args:
            event_id (str): event id
            ticket_type (str): ticket type
            price (float): price
            quantity_available (int): quantity available
        """
        self.event_id = event_id
        self.ticket_type = ticket_type
        self.price = price
        self.quantity_available = quantity_available

    def serialize(self):
        """
        Serialize the ticket model
        """
        return {
            'ticket_id': self.ticket_id,
            'event_id': self.event_id,
            'ticket_type': self.ticket_type,
            'price': self.price,
            'quantity_available': self.quantity_available
        }
