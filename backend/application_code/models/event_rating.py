#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
import uuid
from application_code import db
from datetime import datetime


class EventRating(db.Model):
    """
    Defines Event Rating model
    """
    __tablename__ = 'event_ratings'

    rating_id = db.Column(db.String(255),
                          default=lambda: str(uuid.uuid4()),
                          primary_key=True)
    event_id = db.Column(db.String(255),
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    user_id = db.Column(db.String(255),
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define many to one relationship with events and users
    event = db.relationship('Event', back_populates='ratings')
    user = db.relationship('User', back_populates='ratings')

    def __init__(self, event_id, user_id, rating):
        """
        Initialize the event rating model

        Args:
            event_id (str): event id
            user_id (str): user id
            rating (int): rating
        """
        self.event_id = event_id
        self.user_id = user_id
        self.rating = rating

    def serialize(self):
        """
        Serialize the event rating model
        """
        return {
            'rating_id': self.rating_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'rating': self.rating,
        }
