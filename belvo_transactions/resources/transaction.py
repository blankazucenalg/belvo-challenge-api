from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from belvo_transactions.connection import get_db
import pandas as pd
import json

bp = Blueprint('transaction', __name__)


@bp.route('/transaction', methods=('GET', 'POST'))
def transaction_list():
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


@bp.route('/transaction/<reference>', methods=['GET'])
def transaction(reference):
    tx = fetch_transaction(reference)
    if tx is None:
        abort(404, f'Transaction with reference `{reference}` not found.')
    return jsonify(dict(tx))


def filter_transactions(transaction_list):
    filtered_transactions = []
    uniqueness_check = {}
    for t in transaction_list:
        # Check transaction is valid and is not duplicated (in db and bulk)
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
    return get_db().execute('SELECT * FROM user_transaction WHERE reference = ?', (reference, )).fetchone()


def get_transactions_summary_from_user(user_id, date_from, date_to):
    """
    Return summary from user's accounts

    """
    date_statement = ""
    if date_from is not None and date_to is not None:
        date_statement = f" AND date BETWEEN date('{date_from}') and date('{date_to}') "
    statement = f"SELECT account, sum(amount) as amount, type FROM user_transaction WHERE user_id = {user_id} {date_statement} GROUP BY account, type UNION SELECT account, sum(amount) as amount, 'balance' as type FROM user_transaction WHERE user_id = {user_id} {date_statement} GROUP BY account"

    fetch = get_db().execute(statement).fetchall()
    # SQLite desn't support pivot table so this implementation uses dataframe transformation
    summary = [dict(r) for r in fetch]
    df = pd.DataFrame(summary)
    data = df.pivot_table(index='account', columns='type',
                          values='amount', fill_value=0)
    data = data.rename(
        columns={'inflow': 'total_inflow', 'outflow': 'total_outflow'})
    data['account'] = data.index
    return json.loads(data.to_json(orient="records"))


def get_transactions_by_category_from_user(user_id):
    """
    Return summary from user's transactions by category

    """
    db = get_db()
    fetch = db.execute("SELECT sum(amount) as amount, type, category FROM user_transaction WHERE user_id = ? GROUP BY type, category",
                       (user_id,)).fetchall()
    # data transformation
    summary = [dict(r) for r in fetch]
    df = pd.DataFrame(summary)
    data = df.pivot(index='type', columns='category',
                    values='amount')
    return clean_dictionary(json.loads(data.to_json(orient='index')))


def clean_dictionary(d):
    if not isinstance(d, dict):
        return d
    return dict((key, clean_dictionary(value)) for key, value in d.items() if value is not None)
