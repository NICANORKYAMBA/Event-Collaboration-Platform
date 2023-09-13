#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  11 20:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from application_code import db
from application_code.models.event import Event


def create_event():
    """
    Create a new event and add to the database
    """
    data  = request.json

    if not data:
        return jsonify({'message': 'Not input data provide'}), 400

    try:
        new_event = Event(
                event_name=data['event_name'],
                event_date=data['event_date'],
                event_time=data['event_time'],
                location=data['location'],
                description=data['description']
                )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({'message': 'Event created successfully',
                        'event_id': new_event.event_id}), 201
    except IntegrityError:
        return jsonify({'message': 'Event already exists'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred',
                        'error': str(e)}), 500
