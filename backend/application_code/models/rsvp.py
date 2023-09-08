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
