#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  13 11:00:00 2023

@Author: Nicanor Kyamba

Unittest for auth contoller module
"""
import unittest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from application_code import create_app, db
from application_code.models.user import User
from application_code.controllers.auth_controller import (
        register_user,
        login_user,
        list_users,
        get_user,
        update_user,
        delete_user,
        )
from application_code.config import TestConfig


class AuthControllerTestCase(unittest.TestCase):
    """
    Test case for auth controller
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        """
        Test register user
        """
        response = self.client().post(
            '/api/v1/auth/register',
            json={
                'username': 'testuser',
                'email': 'b1t1S@example.com',
                'password': 'testuser',
                }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'User created successfully')

    def test_register_user_invalid_email(self):
        """
        Test invalid user inputs
        """
        response = self.client().post(
            '/api/v1/auth/register',
            json={
                'username': 'testuser',
                'email': 'testuser',
                'password': 'testuser',
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'Invalid email address')

    def test_register_user_existing_email(self):
        """
        Test registering a user with the same email
        """
        existing_user = User(
                username='existing_user',
                email='existing@example.com',
                password='existing_user'
                )
        db.session.add(existing_user)
        db.session.commit()

        response = self.client().post(
            '/api/v1/auth/register',
            json={
                'username': 'existing_user',
                'email': 'existing@example.com',
                'password': 'existing_user',
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'Email address already in use')

    def test_register_user_no_input_data(self):
        """
        Test registering a user with no input data
        """
        response = self.client().post(
            '/api/v1/auth/register',
            json={}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'No input data provided')


if __name__ == '__main__':
    unittest.main()
