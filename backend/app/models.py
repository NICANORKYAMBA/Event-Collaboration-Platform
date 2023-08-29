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


class User(Base):
    """
    Defines User model
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    profile_image = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Define one to many relationship with events
    events = relationship('Event', back_populates='organizer')
    collaborations = relationship('EventCollaborator', back_populates='user')
    rsvps = relationship('RSVP', back_populates='user')
    comments = relationship('EventComment', back_populates='user')
    ratings = relationship('EventRating', back_populates='user')


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


class EventCollaborator(Base):
    """
    Defines Event Collaborator model
    """
    __tablename__ = 'event_collaborators'

    collaborator_id = Column(Integer, primary_key=True)
    event_id = Column(Integer,
                      ForeignKey('events.event_id'),
                      nullable=False)
    user_id = Column(Integer,
                     ForeignKey('users.user_id'),
                     nullable=False)
    role = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define many to one relationship with events and users
    event = relationship('Event', back_populates='collaborators')
    user = relationship('User', back_populates='collaborations')


class Ticket(Base):
    """
    Defines Tickets model
    """
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True)
    event_id = Column(Integer,
                      ForeignKey('events.event_id'),
                      nullable=False)
    ticket_type = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity_available = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Define many to one relationship with events
    event = relationship('Event', back_populates='tickets')
    rsvps = relationship('RSVP', back_populates='ticket')


class RSVP(Base):
    """
    Defines RSVP model
    """
    __tablename__ = 'rsvps'

    rsvp_id = Column(Integer, primary_key=True)
    event_id = Column(Integer,
                      ForeignKey('events.event_id'),
                      nullable=False)
    user_id = Column(Integer,
                     ForeignKey('users.user_id'),
                     nullable=False)
    ticket_id = Column(Integer,
                       ForeignKey('tickets.ticket_id'),
                       nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define many to one relationship with events, users and tickets
    event = relationship('Event', back_populates='rsvps')
    user = relationship('User', back_populates='rsvps')
    ticket = relationship('Ticket', back_populates='rsvps')


class EventComment(Base):
    """
    Defines Event Comment model
    """
    __tablename__ = 'event_comments'

    comment_id = Column(Integer, primary_key=True)
    event_id = Column(Integer,
                      ForeignKey('events.event_id'),
                      nullable=False)
    user_id = Column(Integer,
                     ForeignKey('users.user_id'),
                     nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define many to one relationship with events and users
    event = relationship('Event', back_populates='comments')
    user = relationship('User', back_populates='comments')


class EventRating(Base):
    """
    Defines Event Rating model
    """
    __tablename__ = 'event_ratings'

    rating_id = Column(Integer, primary_key=True)
    event_id = Column(Integer,
                      ForeignKey('events.event_id'),
                      nullable=False)
    user_id = Column(Integer,
                     ForeignKey('users.user_id'),
                     nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define many to one relationship with events and users
    event = relationship('Event', back_populates='ratings')
    user = relationship('User', back_populates='ratings')
