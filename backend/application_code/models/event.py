#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from sqlalchemy import Column, Integer, String, ForeignKey, \
        DateTime, Date, Time, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Event(Base):
    """
    Defines Events model
    """
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text)
    organizer_id = Column(Integer,
                          ForeignKey('users.user_id'),
                          nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Define a many to one relationship with users (organizer)
    organizer = relationship('User', back_populates='events')
    collaborators = relationship('EventCollaborator', back_populates='event')
    tickets = relationship('Ticket', back_populates='event')
    rsvps = relationship('RSVP', back_populates='event')
    comments = relationship('EventComment', back_populates='event')
    ratings = relationship('EventRating', back_populates='event')
