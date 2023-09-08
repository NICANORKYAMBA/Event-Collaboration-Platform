#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from application_code import db
from datetime import datetime
from application_code.models.event import Event
from application_code.models.user import User


class Ticket(db.Model):
    """
    Defines Tickets model
    """
    __tablename__ = 'tickets'

    ticket_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    ticket_type = db.Column(String(255), nullable=False)
    price = db.Column(Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Define many to one relationship with events
    event = relationship('Event', back_populates='tickets')
    rsvps = relationship('RSVP', back_populates='ticket')

    def __init__(self, event_id, ticket_type, price, quantity_available):
        """
        Initialize the ticket model

        Args:
                event_id (_type_): _description_
                ticket_type (_type_): _description_
                price (_type_): _description_
                quantity_available (_type_): _description_
        """
        self.event_id = event_id
        self.ticket_type = ticket_type
        self.price = price
        self.quantity_available = quantity_available
