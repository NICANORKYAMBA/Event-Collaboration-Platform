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

engine = create_engine(URL, echo=False)


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

        saved_event = self.session.query(Event).first()
        self.assertIsNotNone(saved_event)
        self.assertEqual(saved_event.event_name, 'Alx hackathon')

    def test_event_collaborator_model(self):
        """
        Test event collaborator creation
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

        existing_event = self.session.query(Event).filter_by(
                event_name='Alx hackathon').first()

        if not existing_event:
            event = Event(
                    event_name='Alx hackathon',
                    event_date=datetime(2023, 8, 30).date(),
                    event_time=datetime(2023, 8, 30, 10, 0).time(),
                    location='Nairobi',
                    description='A hackathon',
                    organizer_id=user.user_id
            )
            self.session.add(event)
            self.session.commit()
        else:
            event = existing_event

        collaborator = EventCollaborator(
                event_id=event.event_id,
                user_id=existing_user.user_id,
                role='Organizer'
        )
        self.session.add(collaborator)
        self.session.commit()

        saved_collaborator = self.session.query(EventCollaborator).first()
        self.assertIsNotNone(saved_collaborator)
        self.assertEqual(saved_collaborator.role, 'Organizer')

    def test_ticket_model(self):
        """
        Test ticket creation
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

        existing_event = self.session.query(Event).filter_by(
                event_name='Alx hackathon').first()

        if not existing_event:
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
        else:
            event = existing_event

        ticket = Ticket(
                event_id=event.event_id,
                ticket_type='General Admission',
                price=100.00,
                quantity_available=100
        )
        self.session.add(ticket)
        self.session.commit()

        saved_ticket = self.session.query(Ticket).first()
        self.assertIsNotNone(saved_ticket)
        self.assertEqual(saved_ticket.ticket_type, 'General Admission')

    def test_rsvp_model(self):
        """
        Test RSVP creation
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

        existing_event = self.session.query(Event).filter_by(
                event_name='Alx hackathon').first()

        if not existing_event:
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
        else:
            event = existing_event

        existing_ticket = self.session.query(Ticket).filter_by(
                ticket_type='General Admission').first()

        if not existing_ticket:
            ticket = Ticket(
                    event_id=event.event_id,
                    ticket_type='General Admission',
                    price=100.00,
                    quantity_available=100
            )
            self.session.add(ticket)
            self.session.commit()
        else:
            ticket = existing_ticket

        rsvp = RSVP(
            event_id=event.event_id,
            user_id=existing_user.user_id,
            ticket_id=ticket.ticket_id
            )
        self.session.add(rsvp)
        self.session.commit()

        saved_rsvp = self.session.query(RSVP).first()
        self.assertIsNotNone(saved_rsvp)
        self.assertEqual(saved_rsvp.ticket.ticket_type, 'General Admission')

    def test_event_comment_model(self):
        """
        Test event comment creation
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

        existing_event = self.session.query(Event).filter_by(
                event_name='Alx hackathon').first()

        if not existing_event:
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
        else:
            event = existing_event

        comment = EventComment(
                event_id=event.event_id,
                user_id=existing_user.user_id,
                comment_text='Greatest Event Ever'
        )
        self.session.add(comment)
        self.session.commit()

        saved_comment = self.session.query(EventComment).first()
        self.assertIsNotNone(saved_comment)
        self.assertEqual(saved_comment.comment_text, 'Greatest Event Ever')

    def test_event_rating_model(self):
        """
        Test event rating creation
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

        existing_event = self.session.query(Event).filter_by(
                event_name='Alx hackathon').first()

        if not existing_event:
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
        else:
            event = existing_event

        rating = EventRating(
                event_id=event.event_id,
                user_id=existing_user.user_id,
                rating=5
        )
        self.session.add(rating)
        self.session.commit()

        saved_rating = self.session.query(EventRating).first()
        self.assertIsNotNone(saved_rating)
        self.assertEqual(saved_rating.rating, 5)


if __name__ == '__main__':
    unittest.main()
