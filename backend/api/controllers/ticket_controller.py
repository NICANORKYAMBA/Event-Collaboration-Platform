#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  29 12:00:00 2023

@Author: Nicanor Kyamba
"""
from flask import request, jsonify
from api import db
from api .models.ticket import Ticket
from api.controllers.event_controller import get_event


def create_ticket(event_id):
    """
    Create a ticket for an event

    Args:
        event_id (int): event id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        ticket_type = data['ticket_type']
        price = data['price']
        quantity_available = data['quantity_available']

        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        new_ticket = Ticket(
            event_id=event_id,
            ticket_type=ticket_type,
            price=price,
            quantity_available=quantity_available
        )

        db.session.add(new_ticket)
        db.session.commit()

        return jsonify({
            'message': 'Ticket created successfully',
            'ticket_id': new_ticket.ticket_id
        }), 201
    except Exception as e:
        return jsonify({
            'message': 'An error occurred creating the ticket',
            'error': str(e)
        }), 500


def get_tickets(event_id):
    """
    Get all tickets for an event

    Args:
        event_id (int): event id
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({'message': 'Event not found'}), 404

        tickets = Ticket.query.filter_by(event_id=event_id).all()

        if not tickets:
            return jsonify({'message': 'No tickets found for this event'}), 404

        ticket_list = [ticket.serialize() for ticket in tickets]

        return jsonify({
            'message': 'Tickets retrieved successfully',
            'tickets': ticket_list
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the tickets',
            'error': str(e)
        }), 500


def get_ticket(event_id, ticket_id):
    """
    Get a ticket for an event

    Args:
        event_id (int): event id
        ticket_id (int): ticket id
    """
    try:
        ticket = Ticket.query.filter_by(
                event_id=event_id, ticket_id=ticket_id).first()

        if not ticket:
            return jsonify({'message': 'Ticket not found'}), 404

        return jsonify({
            'message': 'Ticket retrieved successfully',
            'ticket': ticket.serialize()
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred retrieving the ticket',
            'error': str(e)
        }), 500


def update_ticket(event_id, ticket_id):
    """
    Update a ticket for an event

    Args:
        event_id (int): event id
        ticket_id (int): ticket id
    """
    data = request.json

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        ticket = Ticket.query.filter_by(
                event_id=event_id, ticket_id=ticket_id).first()

        if not ticket:
            return jsonify({'message': 'Ticket not found'}), 404

        ticket_type = data['ticket_type']
        price = data['price']
        quantity_available = data['quantity_available']

        if ticket_type:
            ticket.ticket_type = ticket_type
        if price:
            ticket.price = price
        if quantity_available:
            ticket.quantity_available = quantity_available

        db.session.commit()

        return jsonify({
            'message': 'Ticket updated successfully',
            'ticket_id': ticket.ticket_id
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'An error occurred updating the ticket',
            'error': str(e)
        }), 500


def delete_ticket(event_id, ticket_id):
    """
    Delete a ticket for an event

    Args:
        event_id (int): event id
        ticket_id (int): ticket id
    """
    try:
        ticket = Ticket.query.filter_by(
                event_id=event_id, ticket_id=ticket_id).first()

        if not ticket:
            return jsonify({'message': 'Ticket not found'}), 404

        db.session.delete(ticket)
        db.session.commit()

        return jsonify({
            'message': 'Ticket deleted successfully',
            'ticket_id': ticket.ticket_id
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'An error occurred deleting the ticket',
            'error': str(e)
        }), 500
