#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  13 11:00:00 2023

@Author: Nicanor Kyamba

Unittest for auth contoller module
"""
import unittest
import bcrypt
from unittest import mock
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

    def test_login_user(self):
        """
        Test login user
        """
        test_user = User(
                username='testuser',
                email='test@example.com',
                password=bcrypt.hashpw(
                    'testuser'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        db.session.add(test_user)
        db.session.commit()

        response = self.client().post(
            '/api/v1/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'testuser',
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'User logged in successfully')
        self.assertTrue('token' in data)

    def test_login_user_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        response = self.client().post(
            '/api/v1/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'invalid_password',
            }
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['message'], 'Invalid email or password')

    def test_login_user_no_input_data(self):
        """
        Test user login with no input data
        """
        response = self.client().post(
            '/api/v1/auth/login',
            json={}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'No input data provided')

    def test_list_no_users_found(self):
        """
        Test listing all users when no users found
        """
        response = self.client().get('/api/v1/auth/users')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['message'], 'No users found')

    def test_list_users(self):
        """
        Test listing all users
        """
        user1 = User(
                username='testuser',
                email='test@example.com',
                password=bcrypt.hashpw(
                    'testuser'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        user2 = User(
                username='testuser2',
                email='test2@example.com',
                password=bcrypt.hashpw(
                    'testuser2'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        user3 = User(
                username='testuser3',
                email='test3@example.com',
                password=bcrypt.hashpw(
                    'testuser3'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        response = self.client().get('/api/v1/auth/users')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual('users' in data, True)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['username'], 'testuser')
        self.assertEqual(data[1]['username'], 'testuser2')
        self.assertEqual(data[2]['username'], 'testuser3')
        self.assertEqual(data[0]['email'], 'test@example.com')
        self.assertEqual(data[1]['email'], 'test2@example.com')
        self.assertEqual(data[2]['email'], 'test3@example.com')

    def test_list_users_error(self):
        """
        Test listing users when an error occurs
        """
        with mock.patch(
                'application_code.controllers.auth_controller.User.query.all'
                ) as mock_query:
            mock_query.side_effect = Exception('Simulated error')
            response = self.client().get('/api/v1/auth/users')

        self.assertEqual(response.status_code, 500)

        data = response.get_json()
        self.assertEqual(data['message'], 'An error occurred')

    def test_get_one_user(self):
        """
        Test case for getting a user by their id
        """
        test_user = User(
                username='testuser',
                email='test@example.com',
                password=bcrypt.hashpw(
                    'testuser'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        db.session.add(test_user)
        db.session.commit()

        user_id = str(test_user.user_id)

        response = self.client().get(
                '/api/v1/auth/users/{}'.format(user_id))

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue('user' in data)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')

    def test_get_user_not_found(self):
        """
        Test retrieving a non-existent user by user_id
        """
        response = self.client().get('/api/v1/auth/users/9999')

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['message'], 'User not found')

    def test_get_user_error(self):
        """
        Test retrieving a user when an error occurs
        """
        with mock.patch(
                'application_code.controllers.auth_controller.User.query.get'
                ) as mock_query:
            mock_query.side_effect = Exception('Simulated error')
            response = self.client().get('/api/v1/auth/users/9999')

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['message'], 'An error occurred')

    def test_update_user(self):
        """
        Test updating a user
        """
        test_user = User(
                username='testuser',
                email='test@example.com',
                password=bcrypt.hashpw(
                    'testuser'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        db.session.add(test_user)
        db.session.commit()

        user_id = str(test_user.user_id)

        response = self.client().put(
            '/api/v1/auth/users/{}'.format(user_id),
            json={
                'username': 'testuser2',
                'email': 'test2@example.com',
                'password': 'testuser2',
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'User updated successfully')

    def test_update_user_invalid_credentials(self):
        """
        Test updating a user with invalid credentials
        """
        response = self.client().put(
            '/api/v1/auth/users/9999/update',
            json={
                'username': 'testuser2',
                'email': 'test2@example.com',
                'password': 'testuser2',
            }
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['message'], 'Invalid email or password')

    def test_update_user_no_input_data(self):
        """
        Test updating a user with no input data
        """
        response = self.client().put(
            '/api/v1/auth/users/9999/update',
            json={}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'No input data provided')

    def test_update_user_error(self):
        """
        Test updating a user when an error occurs
        """
        with mock.patch(
                'application_code.controllers.auth_controller.User.query.get'
                ) as mock_query:
            mock_query.side_effect = Exception('Simulated error')
            response = self.client().put(
                '/api/v1/auth/users/9999/update',
                json={
                    'username': 'testuser2',
                    'email': 'test2@example.com',
                    'password': 'testuser2',
                }
            )

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['message'], 'An error occurred')

    def test_delete_user(self):
        """
        Test deleting a user
        """
        test_user = User(
                username='testuser',
                email='test@example.com',
                password=bcrypt.hashpw(
                    'testuser'.encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8')
                )
        db.session.add(test_user)
        db.session.commit()

        user_id = str(test_user.user_id)

        response = self.client().delete(
            '/api/v1/auth/users/{}/delete'.format(user_id)

            json={
                'confirm': True
                }
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'User deleted successfully')

    def test_delete_user_no_input(self):
        """
        Test deleting user no credentials provided
        """
        response = self.client().delete(
            '/api/v1/auth/users/9999/delete',
            json={}
        )

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'No input data provided')

    def test_delete_user_error(self):
        """
        Test deleting a user when an error occurs
        """
        with mock.patch(
                'application_code.controllers.auth_controller.User.query.get'
                ) as mock_query:
            mock_query.side_effect = Exception('Simulated error')
            response = self.client().delete(
                '/api/v1/auth/users/9999/delete',
                json={}
            )

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['message'], 'An error occurred')


if __name__ == '__main__':
    unittest.main()
