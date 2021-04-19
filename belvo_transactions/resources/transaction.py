from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from belvo_transactions.connection import get_db
import pandas as pd
import json

bp = Blueprint('transaction', __name__)


@bp.route('/transaction', methods=('GET', 'POST'))
def transaction():
    if request.method == 'POST':
        """
        Create new transactions
        """
        transactions = request.json
        print(transactions)
        if isinstance(transactions, dict):
            transactions = [transactions]
        valid_bulk = filter_transactions(transactions)

        create_transactions_bulk(valid_bulk)

    db = get_db()
    transactions = db.execute('SELECT * FROM user_transaction').fetchall()
    return jsonify([dict(r) for r in transactions])


def filter_transactions(transaction_list):
    filtered_transactions = []
    uniqueness_check = {}
    for t in transaction_list:
        if is_valid(t) and t['reference'] not in uniqueness_check:
            filtered_transactions.append(t)
            uniqueness_check[t['reference']] = True
    return filtered_transactions


def is_valid(transaction):
    if 'reference' not in transaction:
        return False
    elif 'account' not in transaction:
        return False
    elif 'date' not in transaction:
        return False
    elif 'amount' not in transaction:
        return False
    elif 'type' not in transaction:
        return False
    elif 'category' not in transaction:
        return False
    elif 'user_id' not in transaction:
        return False
    elif fetch_transaction(transaction["reference"]) is not None:
        return False
    else:
        try:
            tmp = float(transaction['amount'])
        except:
            return False
        return True


def create_transactions_bulk(transactions):
    db = get_db()
    statement = 'INSERT INTO user_transaction (reference, account, date, amount, type, category, user_id) VALUES '
    for idx, t in enumerate(transactions):
        statement += f"('{t['reference']}', '{t['account']}', date('{t['date']}'), {float(t['amount'])}, '{t['type']}', '{t['category']}', {int(t['user_id'])})"
        if idx < len(transactions) - 1:
            statement += ', '
    print(statement)
    db.execute(statement)
    db.commit()


def fetch_transaction(reference):
    db = get_db()
    return db.execute('SELECT * FROM user_transaction WHERE reference = ?', (reference, )).fetchone()
