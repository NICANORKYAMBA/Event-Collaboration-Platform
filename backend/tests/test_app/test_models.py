#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 15:00:00 2023

@Author: Nicanor Kyamba

Unittests for mysql models
"""
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Event, EventCollaborator,\
        Ticket, RSVP, EventComment, EventRating


URL = 'mysql+mysqldb://nicanorkyamba:NICmakya98@localhost:5000/events_test_database'

engine = create_engine(URL, echo=True)


class TestModels(unittest.TestCase):
    """Test models"""
    def setUp(self):
        """
        Test database and tables creation
        """
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

        Base.metadata.create_all(engine)

    def tearDown(self):
        """
        Rollback the transaction and close the session
        after each test
        """
        self.session.rollback()
        self.session.close()

    def test_user_model(self):
        """
        Test user creation
        """
        existing_user = self.session.query(User).filter_by(
                email='johndoe@me.com').first()

        if not existing_user:
            user = User(
                username='John Doe',
                email='johndoe@me.com',
                password='testpassword'
            )
            self.session.add(user)
            self.session.commit()
        else:
            user = existing_user

        saved_user = self.session.query(User).filter_by(
                username='John Doe').first()

        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'johndoe@me.com')

    def test_event_model(self):
        """
        Test event creation
        """
        existing_user = self.session.query(User).filter_by(
                email='johndoe@me.com').first()

        if not existing_user:
            existing_user = User(
                    username='John Doe',
                    email='johndoe@me.com',
                    password='testpassword'
                    )
            self.session.add(existing_user)
            self.session.commit()

        event = Event(
                event_name='Alx hackathon',
                event_date=datetime(2023, 8, 30).date(),
                event_time=datetime(2023, 8, 30, 10, 0).time(),
                location='Nairobi',
                description='A hackathon',
                organizer_id=existing_user.user_id
                )

        self.session.add(event)
        self.session.commit()

        # Query event and assert that it exists
        saved_event = self.session.query(Event).first()
        self.assertIsNotNone(saved_event)
        self.assertEqual(saved_event.event_name, 'Alx hackathon')


if __name__ == '__main__':
    unittest.main()
