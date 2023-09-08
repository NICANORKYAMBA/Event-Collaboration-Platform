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
