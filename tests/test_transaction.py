import json

transactions_data = [
    {
        "reference": "000051",
        "account": "C00099",
        "date": "2020-01-03",
        "amount": "-51.13",
        "type": "outflow",
        "category": "groceries",
        "user_id": 1
    },
    {
        "reference": "000052",
        "account": "C00099",
        "date": "2020-01-10",
        "amount": "2500.72",
        "type": "inflow",
        "category": "salary",
        "user_id": 1
    },
    {
        "reference": "000053",
        "account": "C00099",
        "date": "2020-01-10",
        "amount": "-150.72",
        "type": "outflow",
        "category": "transfer",
        "user_id": 1
    },
    {
        "reference": "000054",
        "account": "C00099",
        "date": "2020-01-13",
        "amount": "-560.00",
        "type": "outflow",
        "category": "rent",
        "user_id": 1
    },
    {
        "reference": "000051",
        "account": "C00099",
        "date": "2020-01-04",
        "amount": "-51.13",
        "type": "outflow",
        "category": "other",
        "user_id": 1
    },
    {
        "reference": "000689",
        "account": "S00012",
        "date": "2020-01-10",
        "amount": "150.72",
        "type": "inflow",
        "category": "savings",
        "user_id": 1
    }
]


def test_empty_db(client):
    response = client.get('/transaction')
    assert b'[]' in response.data


def test_post_transactions(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/transaction', json=transactions_data
                           )
    assert response.status_code == 200


def test_transactions_summary(client):
    client.post('/transaction', json=transactions_data)
    response = client.get('/user/1/transactions_summary')
    assert response.status_code == 200
    assert b'[{"account":"C00099","balance":1738.87,"total_inflow":2500.72,"total_outflow":-761.85},{"account":"S00012","balance":150.72,"total_inflow":150.72,"total_outflow":0.0}]' in response.data


def test_transactions_summary_filter_date(client):
    client.post('/transaction', json=transactions_data)
    response = client.get('/user/1/transactions_summary',
                          query_string={'date_from': '2020-01-10', 'date_to': '2020-01-10'})
    assert response.status_code == 200
    assert b'[{"account":"C00099","balance":2350.0,"total_inflow":2500.72,"total_outflow":-150.72},{"account":"S00012","balance":150.72,"total_inflow":150.72,"total_outflow":0.0}]' in response.data


def test_transactions_by_categories(client):
    client.post('/transaction', json=transactions_data)
    response = client.get('/user/1/transactions_by_category')
    assert response.status_code == 200
    assert b'{"inflow":{"salary":2500.72,"savings":150.72},"outflow":{"groceries":-51.13,"rent":-560.0,"transfer":-150.72}}' in response.data
