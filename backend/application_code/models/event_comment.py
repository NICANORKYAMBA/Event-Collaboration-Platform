#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from application_code import db
from application_code.models.event import Event
from application_code.models.user import User
from datetime import datetime


class EventComment(db.Model):
    """
    Defines Event Comment model
    """
    __tablename__ = 'event_comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define many to one relationship with events and users
    event = db.relationship('Event', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

    def __init__(self, event_id, user_id, comment_text):
        """
        Initialize the event comment model
        """
        self.event_id = event_id
        self.user_id = user_id
        self.comment_text = comment_text
