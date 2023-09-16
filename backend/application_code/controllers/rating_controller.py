#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  15 14:00:00 2023

@Author: Nicanor Kyamba

@description:
    rating controller
"""
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from application_code import db
from application_code.models.event_rating import EventRating
from application_code.models.event import Event
from application_code.controllers.auth_controller import get_user
from application_code.controllers.event_controller import get_event


def create_rating(event_id):
    """
    Create a rating for an event

    Args:
        event_id (int): id of the event
    """
    data = request.json

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        user_id = get_jwt_identity()
        rating_value = data["rating"]

        event = get_event(event_id)

        if not event:
            return jsonify({"message": "Event not found"}), 404

        existing_rating = EventRating.query.filter_by(
            user_id=user_id, event_id=event_id
        ).first()

        if existing_rating:
            return jsonify({
                "message": "User has already rated  this event"
                }), 400

        new_rating = EventRating(
            event_id=event_id,
            user_id=user_id,
            rating=rating_value,
        )

        db.session.add(new_rating)
        db.session.commit()

        return jsonify({
            "message": "Rating created successfully",
            "rating_id": new_rating.rating_id,
        }), 201

    except Exception as e:
        return jsonify({
            'mesage': 'An error occurred creating the rating',
            'error': str(e)
        }), 500


def get_ratings(event_id):
    """
    Get all ratings for an event

    Args:
        event_id (int): id of the event
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({"message": "Event not found"}), 404

        ratings = EventRating.query.filter_by(event_id=event_id).all()

        if ratings:
            rating_list = [rating.serialize() for rating in ratings]

            return jsonify({
                'message': 'Ratings retrieved successfully',
                'ratings': rating_list
                }), 200

        return jsonify({
            'message': 'No ratings found for this event'
        }), 404

    except Exception as e:
        return jsonify({
            'mesage': 'An error occurred retrieving the ratings',
            'error': str(e)
        }), 500


def get_rating(event_id, rating_id):
    """
    Get a rating for an event

    Args:
        event_id (int): id of the event
        rating_id (int): id of the rating
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({"message": "Event not found"}), 404

        rating = EventRating.query.filter_by(
            rating_id=rating_id, event_id=event_id
        ).first()

        if rating:
            return jsonify({
                'message': 'Rating retrieved successfully',
                'rating': rating.serialize()
            }), 200

        return jsonify({
            'message': 'Rating not found'
        }), 404

    except Exception as e:
        return jsonify({
            'mesage': 'An error occurred retrieving the rating',
            'error': str(e)
        }), 500


def update_rating(event_id, rating_id):
    """
    Update a rating for an event

    Args:
        event_id (int): id of the event
        rating_id (int): id of the rating
    """
    data = request.json

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        event = get_event(event_id)

        if not event:
            return jsonify({"message": "Event not found"}), 404

        existing_rating = EventRating.query.filter_by(
            rating_id=rating_id, event_id=event_id
        ).first()

        if not existing_rating:
            return jsonify({"message": "Rating not found"}), 404

        rating = data["rating"]

        if rating:
            existing_rating.rating = rating

        db.session.commit()

        return jsonify({
            "message": "Rating updated successfully",
            "rating_id": existing_rating.rating_id
        }), 200

    except Exception as e:
        return jsonify({
            'mesage': 'An error occurred updating the rating',
            'error': str(e)
        }), 500


def delete_rating(event_id, rating_id):
    """
    Delete a rating for an event

    Args:
        event_id (int): id of the event
        rating_id (int): id of the rating
    """
    try:
        event = get_event(event_id)

        if not event:
            return jsonify({"message": "Event not found"}), 404

        rating = EventRating.query.filter_by(
            rating_id=rating_id, event_id=event_id
        ).first()

        if rating:
            db.session.delete(rating)
            db.session.commit()

            return jsonify({
                "message": "Rating deleted successfully",
                "rating_id": rating.rating_id
            }), 200

        return jsonify({
            'message': 'Rating not found'
        }), 404

    except Exception as e:
        return jsonify({
            'mesage': 'An error occurred deleting the rating',
            'error': str(e)
        }), 500
