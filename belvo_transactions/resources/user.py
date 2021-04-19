from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from belvo_transactions.connection import get_db
from belvo_transactions.resources.transaction import get_transactions_summary_from_user

bp = Blueprint('user', __name__)


@bp.route('/user', methods=('GET', 'POST'))
def user_list():
    """
    Return all users or create one
    """
    if request.method == 'POST':
        """
        Create a user
        """
        user = request.json
        if 'name' not in user:
            abort(400, 'Name is required.')
        elif 'email' not in user:
            abort(400, 'Email is required.')
        elif get_by_email(user['email']) is not None:
            abort(409, 'There is already an user with that email.')
        else:
            create_user(user)
            inserted_value = get_by_email(user['email'])
            return jsonify(dict(inserted_value))

    users = fetch_users()
    return jsonify([dict(r) for r in users])


@bp.route('/user/<user_id>', methods=('GET', 'PUT'))
def user(user_id):
    """
    Return all users or create one
    """
    if request.method == 'PUT':
        """
        Update a user
        """
        user = request.json
        if 'name' not in user:
            abort(400, 'Name is required.')
        elif 'email' not in user:
            abort(400, 'Email is required.')

        else:
            update_user(user_id, user)
            inserted_value = get_by_email(user['email'])
            return jsonify(dict(inserted_value))

    user = fetch_user(user_id)
    if user is None:
        abort(404, 'User not found')
    return jsonify(dict(user))


@bp.route('/user/<user_id>/transactions_summary', methods=['GET'])
def transactions_summary(user_id):
    """
    Return user's transactions summary
    """
    transactions_summary = get_transactions_summary_from_user(user_id)
    return jsonify(transactions_summary)


def create_user(user):
    db = get_db()
    db.execute(
        'INSERT INTO user (name, email, age) VALUES (?, ?, ?)', (user['name'], user['email'], user['age']))
    return db.commit()


def get_by_email(email):
    return get_db().execute(
        'SELECT * FROM user WHERE email = ?', (email, )).fetchone()


def fetch_user(email):
    return get_db().execute(
        'SELECT * FROM user WHERE id = ?', (email, )).fetchone()


def update_user(user_id, user):
    db = get_db()
    db.execute(
        'UPDATE TABLE user SET name=?, email=?, age=? WHERE id = ?', (user['name'], user['email'], user['age'], user_id))
    return db.commit()


def fetch_users():
    db = get_db()
    return db.execute('SELECT id, name, email, age FROM user').fetchall()
