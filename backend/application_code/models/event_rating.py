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
